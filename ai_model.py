from sklearn.ensemble import RandomForestClassifier
import numpy as np

model = RandomForestClassifier()

# نموذج بسيط للتجربة
X_train = [
    [0, 10],
    [1, 500],
    [1, 2000],
    [0, 30]
]

y_train = [
    0,
    1,
    1,
    0
]

model.fit(X_train, y_train)


def predict(vpn_flag, distance):

    prediction = model.predict([[vpn_flag, distance]])

    if prediction[0] == 0:
        return "LEGITIMATE"

    return "SPOOFED"
