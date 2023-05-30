# Tell My Attendance
This small python script to tell your monthly attendance

**Docker build**

Build docker image `docker build -t <name> .` 

### Usage
It is a simple cli app which will accept the below parameters `train.py` file present in `nima/train.py`. The file used below parameters to train the model on either of the Model type(Aesthetic/Technical) or Both of them.

`usage: train_model.py` [-h] [-d DATASET_DIR] [-n MODEL_NAME] [-s SAMPLE_SIZE]`
                      `[-m METRICS] [-t MODEL_TYPE] [-wa AES_WEIGHTS_PATH]`
                      `[-wt TECH_WEIGHTS_PATH] [-b BATCH_SIZE] [-e EPOCHS]`
                      [-v VERBOSE]`

| **flag** | **name**              | **default**    | **help**                                                     |
| -------- | --------------------- | -------------- | ------------------------------------------------------------ |
| *-d*     | *--dataset-dir*       | *DATASET_DIR*  | *Dataset directory.*                                         |
| *-n*     | *--model-name*        | *mobilenet*    | *Model Name to train, view models.json to know available models for training.* |
| *-s*     | *--sample-size*       | *None*         | *Sample size, None for full size.*                           |
| *-m*     | *--metrics*           | *['accuracy']* | *Weights file path, if any.*                                 |
| *-t*     | *--model-type*        | *aesthetic*    | *Model type to train aesthetic/technical/both.*              |
| *-wa*    | *--aes-weights-path*  | *None*         | *Aesthetic Weights file path, if any.*                       |
| *-wt*    | *--tech-weights-path* | *None*         | *Technical Weights file path, if any.*                       |
| *-b*     | *--batch-size*        | *64*           | *Train/Test Batch size*                                      |
| *-e*     | *--epochs*            | *12*           | *Number of epochs, default 10.*                              |
| *-v*     | *--verbose*           | *0*            | *Verbose, default 0*                                         |
|          |                       |                |                                                              |
### Note : This project refers (Luum)[https://expedia.luum.com/commute/calendar] to measure your attendance. Kindly ensure you are logged in an able to open the page. 

