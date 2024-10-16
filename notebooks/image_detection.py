import logging
import torch
import os
import cv2

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all levels

# Remove any existing handlers
if logger.hasHandlers():
    logger.handlers.clear()

# Create a file handler
file_handler = logging.FileHandler('C:/Users/Hp/Desktop/Kifiya/Week7/ETH-MedData-Warehouse/logs/image_detection.log')
file_handler.setLevel(logging.DEBUG)  # Capture all levels in the file

# Create a formatter and set it for the file handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

def detect_and_process_images(model_name: str = 'yolov11',
                              image_folder: str = 'C:/Users/Hp/Desktop/Kifiya/Week7/ETH-MedData-Warehouse/image/photos',
                              num_images: int = 5) -> None:
    """
    Load model, process images, and display/save detection results.
    Args:
        model_name (str): Name of the pre-trained YOLOv11 model to use (default: 'yolov11').
        image_folder (str): Path to the folder containing images to process (default: 'C:/Users/Hp/Desktop/Kifiya/Week7/ETH-MedData-Warehouse/image/photos').
        num_images (int): Number of images to process (default: 5).
    Returns:
        None
    """
    try:
        # Load pre-trained YOLOv11 model
        model = torch.hub.load('ultralytics/yolov11', 'yolov11', pretrained=True)
        logger.info(f"Loaded pre-trained YOLOv11 model: {model_name} successfully")

        # Define output folder for detected images
        output_folder = 'C:/Users/Hp/Desktop/Kifiya/Week7/ETH-MedData-Warehouse/image/testing_detected/detected_images'

        # Create output folder if it does not exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            logger.info(f"Created output folder: {output_folder}")

        # Loop through the first 'num_images' images in the folder
        for i, img_name in enumerate(os.listdir(image_folder)[:num_images]):
            img_path = os.path.join(image_folder, img_name)
            logger.info(f"Processing image: {img_name} ({i+1}/{num_images})")

            try:
                # Read the image
                img = cv2.imread(img_path)

                # Run object detection
                results = model(img)
                logger.debug(f"Ran object detection on image: {img_name}")

                # Show the results
                results.show()

                # Save detection results to output folder
                results.save(save_dir=output_folder)
                logger.info(f"Saved detection results for image: {img_name}")

            except Exception as e:
                logger.error(f"Error processing image {img_name}: {str(e)}")
        logger.info("Image processing completed successfully.")

    except Exception as e:
        logger.error(f"Error loading model or processing images: {str(e)}")
        return None

def extract_detections(model_name: str = 'yolov11',
                      image_folder: str = 'C:/Users/Hp/Desktop/Kifiya/Week7/ETH-MedData-Warehouse/image/photos',
                      num_images: int = 5) -> None:
    """
    Load model, process images, and extract bounding box, class labels, and confidence scores.

    Args:
        model_name (str): Name of the pre-trained YOLOv11 model to use (default: 'yolov11').
        image_folder (str): Path to the folder containing images to process (default: 'C:/Users/Hp/Desktop/Kifiya/Week7/ETH-MedData-Warehouse/image/photos').

    Returns:
        None
    """
    try:
        # Load pre-trained YOLOv11 model
        model = torch.hub.load('ultralytics/yolov11', 'yolov11', pretrained=True)
        logger.info(f"Loaded pre-trained YOLOv11 model: {model_name} successfully")
        output_folder = 'C:/Users/Hp/Desktop/Kifiya/Week7/ETH-MedData-Warehouse/image/testing_detected/detection_results'

        # Create output folder if it does not exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            logger.info(f"Created output folder: {output_folder}")

        # Loop through all images in the folder
        for img_name in os.listdir(image_folder)[:num_images]:
            img_path = os.path.join(image_folder, img_name)

            # Run object detection
            results = model(img_path)

            # Extract detections
            detections = results.pandas().xyxy[0]  # Pandas dataframe of detection results

            # Check if detections is not empty
            if not detections.empty:
                logger.info(f"Detections for {img_name}:")
                logger.info(detections[['name', 'confidence', 'xmin', 'ymin', 'xmax', 'ymax']])

                # Save detections to CSV file
                detections[['name', 'confidence', 'xmin', 'ymin', 'xmax', 'ymax']].to_csv(os.path.join(output_folder, f"{img_name}_detections.csv"), index=False)
                logger.info(f"Saved detection results for image: {img_name}")
            else:
                logger.info(f"No detections found for image: {img_name}")

        logger.info("Detection extraction completed successfully.")

    except Exception as e:
        logger.error(f"Error loading model or extracting detections: {str(e)}")
        return None