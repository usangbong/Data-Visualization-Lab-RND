import tensorflow as tf
import numpy as np
import pandas as pd 
from sklearn.preprocessing import LabelEncoder 

# 학습 데이터 파일 로드
train_dataset_df = pd.read_csv('../data/train.csv') 

# 학습 데이터셋 인코딩
labelencoder=LabelEncoder()

for col in train_dataset_df.columns: 
    train_dataset_df[col] = labelencoder.fit_transform(train_dataset_df[col]) 
x_train = train_dataset_df[train_dataset_df.columns[1:]].to_numpy()
y_train = train_dataset_df[train_dataset_df.columns[0]].to_numpy()
y_train = tf.keras.utils.to_categorical(y_train, num_classes=2)

# 테스트 데이터 파일 로드
test_dataset_df = pd.read_csv('../data/test-1.csv') 

# 테스트 데이터셋 인코딩
labelencoder=LabelEncoder()

for col in test_dataset_df.columns: 
    test_dataset_df[col] = labelencoder.fit_transform(test_dataset_df[col]) 

x_test = test_dataset_df[test_dataset_df.columns[1:]].to_numpy()
y_test = test_dataset_df[test_dataset_df.columns[0]].to_numpy()
y_test = tf.keras.utils.to_categorical(y_test, num_classes=2)

# 모델 생성
model = tf.keras.Sequential([
                             tf.keras.layers.Dense(units=48, activation='relu', input_shape=(22,)),
                             tf.keras.layers.Dense(units=24, activation='relu'),
                             tf.keras.layers.Dense(units=12, activation='relu'),
                             tf.keras.layers.Dense(units=2, activation='sigmoid')
])

# 모델 학습 동작 테스트 - 시험 중 코드 테스트 용도
history = model.fit(x_train, y_train, epochs=25, batch_size=32, validation_split=0.25, callbacks=[tf.keras.callbacks.EarlyStopping(patience=3, monitor='val_loss')])

# 모델 학습 및 준비된 모델 체크포인트 저장(공인 시험 인증 준비 단계) - 시험 중 실행 금지
#checkpoint_path = "../models/trained_model_1/model_1.ckpt"
#cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path, save_weights_only=True,verbose=1)
#history = model.fit(x_train, y_train, epochs=25, batch_size=32, validation_split=0.25, callbacks=[tf.keras.callbacks.EarlyStopping(patience=3, monitor='val_loss'), cp_callback])

# 모델 불러오기 (공인시험인증을 위한 준비된 모델 사용)
checkpoint_path = "../models/trained_model_1/model_1.ckpt"
model.load_weights(checkpoint_path)

# 모델 평가
saveModelEval = model.evaluate(x_test, y_test)
mLoss = saveModelEval[0]
mAcc = saveModelEval[1]
mTP = saveModelEval[2]
mTN = saveModelEval[3]
mFN = saveModelEval[4]
mFP = saveModelEval[5]

# Confusion matrix
print("TP = %f"%mTP)
print("TN = %f"%mTN)
print("FN = %f"%mFN)
print("FP = %f"%mFP)

print("Accuracy = (TP + TN)/(TP + FN + FP + TN))")
print("Accuracy = %f"%mAcc)