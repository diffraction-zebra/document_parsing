from typing import Tuple, List

import pathlib

from PIL import Image
from surya.ocr import run_ocr
from surya.detection import batch_text_detection
from surya.layout import batch_layout_detection
from surya.model.detection import segformer
from surya.model.recognition.model import load_model
from surya.model.recognition.processor import load_processor
from surya.settings import settings


def bbox_inside(bbox_in: Tuple[float, float, float, float],
                bbox_out: Tuple[float, float, float, float]) -> bool:
    x1, y1, x2, y2 = bbox_in
    x3, y3, x4, y4 = bbox_out
    return x3 <= x1 and y3 <= y1 and x4 >= x2 and y4 >= y2


layout_model, layout_processor, det_model, det_processor, rec_model, rec_processor = None, None, None, None, None, None


def load_models():
    layout_checkpoint = settings.LAYOUT_MODEL_CHECKPOINT
    global layout_model, layout_processor, det_model, det_processor, rec_model, rec_processor
    layout_model, layout_processor = (segformer.load_model(checkpoint=layout_checkpoint),
                                      segformer.load_processor(checkpoint=layout_checkpoint))
    det_model, det_processor = segformer.load_model(), segformer.load_processor()
    rec_model, rec_processor = load_model(), load_processor()


def extract_tables_from_image(image_path: pathlib.Path) -> List[str]:
    image = Image.open(image_path)

    # layout detection
    global layout_model, layout_processor, det_model, det_processor, rec_model, rec_processor
    assert layout_model is not None, 'Models are not loaded'

    # layout recognition
    line_predictions = batch_text_detection([image], det_model, det_processor)
    layout_predictions = batch_layout_detection([image], layout_model, layout_processor, line_predictions)

    # text recognition
    langs = ['ru']
    text_predictions = run_ocr([image], [langs], det_model, det_processor, rec_model, rec_processor)

    # TODO? polygon algorithm for fast text chunking
    # find tables labels in layout predictions
    # put all text from one table together

    tables: List[str] = []
    for layout in layout_predictions[0].bboxes:
        if layout.label == 'Table':
            table = []
            for line in text_predictions[0].text_lines:
                if bbox_inside(line.bbox, layout.bbox):
                    table.append(line.text)
            tables.append('\n'.join(table))
    return tables
