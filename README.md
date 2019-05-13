# Deep Session Interest Network

## Operating environment
- python==3.6
- tensorflow-gpu==1.4.0
- deepctr==0.4.0.post0
- numpy==1.15.1
- pandas==0.22.0
- scikit-learn==0.19.2
- tqdm==4.19.5


## Download dataset and preprocess
### Download dataset

1. Download Dataset [Ad Display/Click Data on Taobao.com](https://tianchi.aliyun.com/dataset/dataDetail?dataId=56)
2. Extract the files into the ``raw_data`` directory
   
### Data preprocessing

1. run  `0_gen_sampled_data.py`,
sample the data by user
2. run `1_gen_sessions.py`,
generate historical session sequence for each user

## Training and Evaluation

### Train DIN model
1. run `2_gen_din_input.py`,generate input data
2. run `train_din.py`

### Train DIEN model
1. run `2_gen_dien_input.py`,generate input data(since the code is not optimized, this may take a long time to sample negative samples when setting `DIEN_NEG_SAMPLING = True` in `config.py`)
2. run `train_dien.py`

### Train DSIN model
1. run `2_gen_dsin_input.py`,generate input data
2. run `train_dsin.py`

**If the loss during the training is abnormally large, please restart the training process or change the seed.**