from ultralytics import YOLO

def from_picture(picture_path: str) -> dict:
    def img2str(model_path: str, img_path: str) -> str:
        model = YOLO(model_path)
        res = model(img_path)[0]
        # clear_output()
        dic = res.names
        return dic[res.probs.top1]
    
    kind = img2str('./db/kind2.pt', picture_path)
    dest = img2str('./db/dest2.pt', picture_path)
    sex = img2str('./db/sex.pt', picture_path)
    season = img2str('./db/season.pt', picture_path).replace('Всесезон', 'Всесезон / помещения')
    return {'Тип одежды': kind, 'Назначение': dest, 'Пол и возраст': sex, 'Сезон': season}

from_picture('./images/plane.jpg')