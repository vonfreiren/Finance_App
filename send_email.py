import yagmail

receiver = "your@gmail.com"
body = "Hello there from Yagmail"
filename = "document.pdf"

yag = yagmail.SMTP("my@gmail.com", oauth2_file="~/oauth2_creds.json")
yag.send(
    to=receiver,
    subject="Yagmail test with attachment",
    contents=body, 
)