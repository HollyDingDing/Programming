import tensorflow as tf
import cv2
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, Dense, MaxPooling2D, Flatten, Dropout


def da_createModel():
	model = Sequential(name="da")
	model.add(Conv2D(filters=64, kernel_size=(7, 7), activation="relu"))
	model.add(Conv2D(filters=64, kernel_size=(7, 7), activation="relu"))
	model.add(MaxPooling2D(pool_size=(4, 4)))
	model.add(Conv2D(filters=32, kernel_size=(3, 3), activation="relu"))
	model.add(MaxPooling2D(pool_size=(3, 3)))
	model.add(Flatten())
	model.add(Dense(units=64, activation="relu"))
	model.add(Dropout(rate=0.2))
	model.add(Dense(units=32, activation="relu"))
	model.add(Dense(units=10, activation="softmax"))
	return model

if __name__ == "__main__":
	model = da_createModel()