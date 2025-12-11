


mobile = {
	"codeName": "Mobile",
	"paperheight": "180mm",
	"paperwidth": "90mm",
	"left": "4mm",
	"right": "4mm",
	"top": "0mm",
	"bottom": "4mm",
	"linespread": "1.15"
}

tablet = mobile.copy()
tablet["codeName"] = "Tablet"
tablet["paperheight"] = "240mm"
tablet["paperwidth"] = "140mm"
tablet["left"] = "6mm"
tablet["right"] = "6mm"
tablet["bottom"] = "6mm"
tablet["linespread"] = "1.35"

ipad = mobile.copy()
ipad["codeName"] = "Ipad"
ipad["paperheight"] = "220mm"
ipad["paperwidth"] = "165mm"
ipad["left"] = "6mm"
ipad["right"] = "6mm"
ipad["bottom"] = "6mm"
ipad["linespread"] = "1.35"

a4 = mobile.copy()
a4["codeName"] = "A4"
a4["paperheight"] = "297mm"
a4["paperwidth"] = "210mm"
a4["top"] = "5mm"
a4["left"] = "20mm"
a4["right"] = "20mm"
a4["bottom"] = "15mm"
a4["linespread"] = "1.5"

formats = [mobile, tablet, ipad, a4]
