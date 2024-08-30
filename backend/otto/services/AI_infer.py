from AI_model.app2 import infer

def return_infer_response(b64_image_data):
    infer_data = infer(b64_image_data)
    detected_type = infer_data['detected_type']
    confidence = infer_data['confidence']
    processing_time = infer_data['processing_time']
    inference_response = {
        "detected_type":detected_type,
        "confidence":confidence, 
        "processing_time":processing_time.total_seconds()
    }
    return inference_response