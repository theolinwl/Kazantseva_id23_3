from fastapi import HTTPException
import base64
import numpy as np
import cv2


def clean_base64(encoded_str, add_prefix=False):
    prefix = "data:image/jpeg;base64,"

    if encoded_str.startswith(prefix):
        encoded_str = encoded_str.split(',')[1]

    if add_prefix:
        encoded_str = prefix + encoded_str

    return encoded_str


def get_image_from_base64(encoded_str):
    try:
        np_arr = np.frombuffer(base64.b64decode(encoded_str), np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
        return image
    except Exception:
        raise HTTPException(status_code=400,
                            detail='Failed to decode image')


def get_base64_from_image(image):
    _, buffer = cv2.imencode('.jpeg', image)
    return base64.b64encode(buffer).decode('utf-8')


def otsu_binarization(encoded_str):
    image = get_image_from_base64(encoded_str)
    # _, binary_image = cv2.threshold(
    #     image, 0, 255,
    #     cv2.THRESH_BINARY + cv2.THRESH_OTSU
    # )

    # считаем гистограмму интенсивностей серого изображения
    hist = np.zeros(256, dtype=int)
    for pixel in image.flatten():
        hist[pixel] += 1

    # сумма всех интенсивностей
    intensity_sum = np.sum(image)

    all_pixel_count = image.size
    best_thresh = 0
    best_sigma = float('inf')
    first_class_pixel_count = 0
    first_class_intensity_sum = 0

    for thresh in range(256):
        first_class_pixel_count += hist[thresh]
        first_class_intensity_sum += thresh * hist[thresh]

        first_class_prob = first_class_pixel_count / all_pixel_count
        second_class_prob = 1.0 - first_class_prob

        first_class_mean = first_class_intensity_sum / first_class_pixel_count if first_class_pixel_count != 0 else 0
        second_class_mean = ((intensity_sum - first_class_intensity_sum) /
                             (all_pixel_count - first_class_pixel_count)) if (all_pixel_count - first_class_pixel_count) != 0 else 0

        if first_class_pixel_count != 0:
            first_class_variance = np.sum((image[image < thresh] - first_class_mean) ** 2) / first_class_pixel_count
        else:
            first_class_variance = 0

        if (all_pixel_count - first_class_pixel_count) != 0:
            second_class_variance = np.sum((image[image >= thresh] - second_class_mean) ** 2) / (all_pixel_count - first_class_pixel_count)
        else:
            second_class_variance = 0

        sigma = first_class_prob * first_class_variance + second_class_prob * second_class_variance

        if sigma < best_sigma:
            best_sigma = sigma
            best_thresh = thresh

    _, binary_image = cv2.threshold(
        image, best_thresh, 255,
        cv2.THRESH_BINARY
    )

    result_base64 = get_base64_from_image(binary_image)
    return result_base64
