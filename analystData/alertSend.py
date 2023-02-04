from pypushdeer import PushDeer
from DBhandle import common


sql1 = "SELECT value FROM config WHERE project='pushServer' "
server = common.select(sql1).values[0][0]

sql2 = "SELECT value FROM config WHERE project='pushKey' "
key = common.select(sql2).values[0][0]


def sendAlert(title="Title", message="Message"):
    print("alert sent")
    push = PushDeer(server=server, pushkey=key)
    push.send_text(title, message)


if __name__ == "__main__":
    sendAlert("123", "123")