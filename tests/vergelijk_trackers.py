#!/usr/bin/env python3
"""VTV Jurycoach proef: ByteTrack versus BoT-SORT met ReID, uitsluitend lokaal.
Een zichtbaar track-ID bewijst nog niet dat de juiste gymnast wordt gevolgd.
"""
import argparse, csv, json, math
from pathlib import Path

def select_ids(detections,pins):
    if len(pins)!=2 or len(detections)<2:
        raise ValueError("Er moeten twee verschillende personen gedetecteerd zijn op het startbeeld.")
    def score(box,p):
        x1,y1,x2,y2=box
        w=max(1,x2-x1);h=max(1,y2-y1)
        cx=(x1+x2)/2;cy=(y1+y2)/2
        outside=0 if x1<=p[0]<=x2 and y1<=p[1]<=y2 else 1.5
        return math.hypot((p[0]-cx)/w,(p[1]-cy)/h)+outside
    ranks=sorted((score(a["box"],pins[0])+score(b["box"],pins[1]),i,j)
                 for i,a in enumerate(detections) for j,b in enumerate(detections) if i!=j)
    cost,i,j=ranks[0]
    if cost>2.5:raise ValueError("Aangewezen gymnasten komen onvoldoende overeen met detecties. Kies een ander startbeeld.")
    return [detections[i]["id"],detections[j]["id"]]

def select_pins(frame,folder,pins_file=None):
    import cv2
    if pins_file:
        return [tuple(map(int,p)) for p in json.loads(Path(pins_file).read_text(encoding="utf-8"))["pins"]]
    h,w=frame.shape[:2];scale=min(1,1100/w)
    small=cv2.resize(frame,(round(w*scale),round(h*scale)))
    pins=[];title="Gymnast 1 (blauw) en 2 (roze) kiezen - Enter"
    cv2.namedWindow(title,cv2.WINDOW_NORMAL)
    def click(event,x,y,flags,data):
        if event==cv2.EVENT_LBUTTONDOWN and len(pins)<2:pins.append((int(x/scale),int(y/scale)))
    cv2.setMouseCallback(title,click)
    while True:
        picture=small.copy()
        for i,(x,y) in enumerate(pins):
            color=(255,90,0) if i==0 else (130,40,230)
            cv2.circle(picture,(round(x*scale),round(y*scale)),9,color,-1)
            cv2.putText(picture,str(i+1),(round(x*scale)+9,round(y*scale)),cv2.FONT_HERSHEY_SIMPLEX,.8,color,2)
        cv2.imshow(title,picture)
        key=cv2.waitKey(40)&255
        if key in (13,10) and len(pins)==2:break
        if key in (ord("r"),ord("R")):pins.clear()
        if key==27:raise SystemExit("Selectie afgebroken.")
    cv2.destroyWindow(title)
    (folder/"startselectie.json").write_text(json.dumps({"pins":pins},indent=2),encoding="utf-8")
    return pins

def track_boxes(result):
    b=result.boxes
    if b is None or b.id is None:return []
    xy=b.xyxy.cpu().numpy();ids=b.id.cpu().numpy().astype(int)
    return [{"id":int(i),"box":[float(v) for v in box]} for box,i in zip(xy,ids)]

def botsort_config(folder):
    import yaml
    from ultralytics.utils import ROOT
    source=Path(ROOT)/"cfg"/"trackers"/"botsort.yaml"
    cfg=yaml.safe_load(source.read_text(encoding="utf-8"))
    cfg.update(with_reid=True,model="auto",gmc_method="none")
    dest=folder/"botsort_reid.yaml"
    dest.write_text(yaml.safe_dump(cfg,sort_keys=False),encoding="utf-8")
    return str(dest)

def run_tracker(name,config,args,pins,baseline,folder):
    import cv2
    from ultralytics import YOLO
    cap=cv2.VideoCapture(str(args.video))
    if not cap.isOpened():raise RuntimeError("Kan video niet openen.")
    fps=cap.get(cv2.CAP_PROP_FPS)
    if fps<=0:raise RuntimeError("Geen geldige video-FPS.")
    stride=max(1,round(fps/args.fps))
    cap.set(cv2.CAP_PROP_POS_MSEC,args.start*1000)
    model=YOLO(args.model)
    ids=None;frames=0;rows=[];next_time=args.start
    while True:
        ok,frame=cap.read()
        if not ok:break
        t=(cap.get(cv2.CAP_PROP_POS_FRAMES)-1)/fps
        if t>args.end:break
        frames+=1
        if (frames-1)%stride:continue
        result=model.track(frame,persist=True,tracker=config,classes=[0],
                           conf=args.conf,iou=.7,imgsz=args.imgsz,verbose=False)[0]
        boxes=track_boxes(result)
        if ids is None:
            ids=select_ids(boxes,pins)
            print(name,"start-IDs",ids)
        if t+.5/fps<next_time:continue
        present={b["id"] for b in boxes}
        baseline_row=min(baseline,key=lambda x:abs(x["time"]-t)) if baseline else None
        row={
          "tijd_s":round(t,2),
          "detecties_alle_personen":len(boxes),
          "gymnast_1_ID":ids[0],"gymnast_1_ID_zichtbaar":int(ids[0] in present),
          "gymnast_2_ID":ids[1],"gymnast_2_ID_zichtbaar":int(ids[1] in present),
          "beide_geselecteerde_IDs":int(set(ids).issubset(present)),
          "v126_geselecteerde_poses":baseline_row.get("selectedPeople","") if baseline_row else "",
          "v126_vergelijking_tijd_s":baseline_row.get("time","") if baseline_row else "",
          "controle_echt_dezelfde_2":"","trainer_ten_onrechte_gevolgd":"",
          "persoonswisseling":"","opmerking":""
        }
        rows.append(row)
        if args.snapshots and (len(rows)==1 or len(rows)%max(1,round(args.fps*2))==0):
            img=frame.copy()
            for box in boxes:
                x1,y1,x2,y2=map(round,box["box"])
                color=(255,90,0) if box["id"]==ids[0] else (130,40,230) if box["id"]==ids[1] else (160,160,160)
                cv2.rectangle(img,(x1,y1),(x2,y2),color,3)
                cv2.putText(img,f"ID {box['id']}",(x1,max(20,y1-5)),cv2.FONT_HERSHEY_SIMPLEX,.7,color,2)
            cv2.imwrite(str(folder/f"{name}_{t:07.2f}.jpg"),cv2.resize(img,(960,540)))
        next_time=t+1/args.fps
    cap.release()
    if not rows:raise RuntimeError("Geen trackingmeetpunten geproduceerd.")
    path=folder/f"{name}_metingen.csv"
    with path.open("w",newline="",encoding="utf-8-sig") as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]),delimiter=";")
        writer.writeheader();writer.writerows(rows)
    good=sum(x["beide_geselecteerde_IDs"] for x in rows)
    return {"tracker":name,"model":args.model,"punten":len(rows),
      "beide_start_IDs_aanwezig":good,"percentage_start_IDs_aanwezig":round(100*good/len(rows),1),
      "nog_handmatig_te_controleren":"Track-ID aanwezig bewijst de identiteit niet.",
      "csv":path.name}

def selftest():
    det=[{"id":11,"box":[200,200,350,520]},{"id":22,"box":[700,200,850,520]},
         {"id":33,"box":[480,180,600,560]}]
    assert select_ids(det,[(280,340),(780,360)])==[11,22]
    try:select_ids(det,[(0,0),(780,360)])
    except ValueError:pass
    else:raise AssertionError("Onjuiste startpersoon zou geaccepteerd worden")
    print("Zelftest geslaagd.")

def main():
    p=argparse.ArgumentParser(description="Jurycoach: lokale ByteTrack versus BoT-SORT+ReID proef.")
    p.add_argument("--video",default="Js 9-9.mp4")
    p.add_argument("--reference",default=None)
    p.add_argument("--model",default="yolo26n.pt")
    p.add_argument("--start",type=float,default=50)
    p.add_argument("--end",type=float,default=149.9)
    p.add_argument("--fps",type=float,default=5)
    p.add_argument("--imgsz",type=int,default=960)
    p.add_argument("--conf",type=float,default=.15)
    p.add_argument("--output",default="tracker-resultaten")
    p.add_argument("--pins-file",default=None)
    p.add_argument("--snapshots",action="store_true")
    p.add_argument("--selftest",action="store_true")
    a=p.parse_args()
    if a.selftest:return selftest()
    if not 0<=a.start<a.end or a.fps<=0:p.error("Ongeldige tijd/FPS.")
    import cv2
    folder=Path(a.output);folder.mkdir(parents=True,exist_ok=True)
    v=cv2.VideoCapture(a.video)
    if not v.isOpened():p.error("Video niet gevonden.")
    v.set(cv2.CAP_PROP_POS_MSEC,a.start*1000);ok,frame=v.read();v.release()
    if not ok:p.error("Startbeeld niet leesbaar.")
    pins=select_pins(frame,folder,a.pins_file)
    baseline=json.loads(Path(a.reference).read_text(encoding="utf-8")).get("frames",[]) if a.reference else []
    config=botsort_config(folder)
    outcomes=[]
    for name,setting in [("ByteTrack","bytetrack.yaml"),("BoT-SORT_ReID",config)]:
        try:outcomes.append(run_tracker(name,setting,a,pins,baseline,folder))
        except Exception as exc:
            outcomes.append({"tracker":name,"status":"mislukt","fout":str(exc)})
            print(name,"mislukt:",exc)
    summary={"video":Path(a.video).name,"start_s":a.start,"eind_s":a.end,
             "meetfrequentie_fps":a.fps,"zelfde_detector_en_seed":True,
             "let_op":"Echte gymnastidentiteit, trainerfouten en persoonswisselingen handmatig controleren.",
             "resultaten":outcomes}
    (folder/"vergelijking.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
    print("Resultaten:",(folder/"vergelijking.json").resolve())

if __name__=="__main__":main()
