import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, UpdateView, ListView
from VakSmsApi import VakSmsApi
import requests
from .forms import (
    ProfileForm,
)
from .models import ProfileUser, ProfileOperations

api = VakSmsApi(api_key="c230a5896a6e4ab1a743d07a0340fc78")
API = "c230a5896a6e4ab1a743d07a0340fc78"

a = {
    "OpenAI": "dr",
    "Cupis": "cp",
    "Tinkoff": "tf",
    "QIWl Wallet": "qw",
    "VK - MailRu": "mr",
    "Netflix": "nf",
    "AliExpress": "ai",
    "Юmoney": "ym",
    "Nike": "nk",
    "Protonmail": "pm",
    "WhatsApp": "wa",
    "Twitter": "tw",
    "Yahoo": "yh",
    "Yalla": "ll",
    "AOL": "ao",
    "Discord": "dc",
    "Facebook": "fb",
    "WeChat": "wc",
    "Instagram": "ig",
    "PayPal": "pp",
    "WebMoney": "wm",
    "AirBnb": "ab",
    "Yandex": "ya",
    "Google": "gl",
    "Uber": "ub",
    "Вкусно и точка": "md",
    "Tinder": "td",
    "Telegram": "tg",
    "Line messenger": "lm",
    "Tiktok": "tk",
    "Microsoft": "ms",
    "Viber": "vi",
    "Tencent QQ": "qq",
    "Steam": "st",
    "Coffee LIKE": "ec",
    "Checkscan": "chs",
    "Greggs": "eg",
    "Grindr": "gd",
    "thediversity": "hi",
    "Paysend": "pd",
    "Kraisbonus": "kb",
    "Rencredit": "rc",
    "Золотое Яблоко": "gap",
    "Citilink": "cl",
    "Winelab": "wn",
    "Letual": "le",
    "Технопарк": "tpk",
    "holodilnik.ru": "hld",
    "Mozen": "mz",
    "Weplay": "pw",
    "Epicnpc": "nc",
    "vsesmart": "va",
    "TaxiMaxim": "tm",
    "Casino Online": "co",
    "FixPrice": "fp",
    "stalker-co": "str",
    "remi": "rmi",
    "Lazada": "dl",
    "hh.ru": "hh",
    "bethowen.ru": "bth",
    "salton-promo": "spr",
    "kotanyipromo": "ktn",
    "namars": "mrs",
    "VTB": "vt",
    "internetopros": "io",
    "Ebay": "eb",
    "DiDi taxi": "dd",
    "Twitch": "th",
    "Верный": "vn",
    "Vsesmart.ru": "sar",
    "Amazon": "am",
    "Cstar": "rx",
    "24u": "24u",
    "Coolclever": "cv",
    "Tilda": "ld",
    "Weco": "wo",
    "СберМегаМаркет": "smm",
    "Atlasbus.by": "atl",
    "Vivaldi": "vd",
    "Mobileproxy": "my",
    "Alfa-Bank": "af",
    "SberCloud": "scd",
    "TradingView": "tv",
    "Аптеки": "at",
    "Золотая Корона": "zk",
    "MyBeautyBonus": "yb",
    "Stormgain": "sn",
    "Seafood-shop": "sfs",
    "Getcontact": "gc",
    "ПочтаБанк": "pbk",
    "Apple": "al",
    "ФКХК": "fkhk",
    "Zhihu": "zu",
    "kopilkaclub": "kc",
    "MyGLO": "ae",
    "Кошелек": "cm",
    "Bumble": "bm",
    "Tatneft": "tn",
    "LOVE": "lv",
    "Lukoil": "lkl",
    "Regru": "rr",
    "Taobao": "tb",
    "Ogon": "og",
    "AliPay": "ap",
    "Страховые": "strh",
    "Петрович": "ph",
    "etxt.biz": "txt",
    "Tanuki": "ti",
    "Rutube": "rtb",
    "nloto": "nlt",
    "ЧитайГород": "chg",
    "Ак Барс Банк": "ak",
    "Твоё": "ty",
    "Move": "xc",
    "Веб хостинги": "bg",
    "MVideo": "mv",
    "СберМаркет": "sm",
    "Столото": "sl",
    "Киносервисы": "ks",
    "Raiffeisen": "rf",
    "Onrealt": "or",
    "Вкусвилл": "vv",
    "KFC": "kf",
    "Ашан": "au",
    "Battle": "xn",
    "Signal": "sig",
    "Burger King": "bk",
    "Profi": "prf",
    "Deliveroo": "do",
    "Tom-tailor": "tot",
    "Novex": "nx",
    "Шоколадница": "shc",
    "JumpTaxi": "jt",
    "Premium one": "ta",
    "IQOS": "iqs",
    "Buff.163": "bf",
    "Vodorobot": "vr",
    "budget4me-34": "bgp",
    "Biglion": "bl",
    "Ostin": "on",
    "Спортмастер": "sa",
    "Мята lounge": "mlg",
    "KazanExpress": "ke",
    "Кикшеринг": "sk",
    "banki.ru": "br",
    "ДругВокруг": "dv",
    "Ozon": "oz",
    "KNP24": "kn",
    "Drom": "hz",
    "DoDo pizza": "dp",
    "Avito": "av",
    "Remit": "re",
    "Wildberries": "wb",
    "Inbox lv": "il",
    "X5ID": "x5",
    "Book24": "b24",
    "Marlboro": "mrl",
    "LinkedIn": "ln",
    "Магнит": "mg",
    "IMO messanger": "im",
    "Beela Chat": "ba",
    "Perfluence": "pf",
    "inDriver": "rl",
    "Wooppay": "wp",
    "mail.kz": "mkz",
    "Blablacar": "bb",
    "Steemit": "ste",
    "OLX": "ox",
    "Farpost": "fr",
    "32Red": "rd",
    "Naver": "nv",
    "Unistream": "us",
    "Coinbase": "cb",
    "werewolf.53site": "wer",
    "Getir": "ge",
    "Battle": "bt",
    "FreeCash": "fc",
    "Monese": "me",
    "Rocketreach": "rk",
    "Whitecard": "wt",
    "bet365": "ef",
    "Ticketmaster.com": "tz",
    "Ftx": "fx",
    "Dropverse": "dro",
    "Weststeincard": "wcd",
    "Paysafecard": "pc",
    "Craigslist": "crg",
    "Okcupid": "oc",
    "Yubo": "yu",
    "Сoursehero": "coh",
    "rediff.com": "rdf",
    "GroupMe": "gm",
    "Revolut": "rt",
    "Ultra.io": "uo",
    "4FunLite": "fl",
    "1688": "hn",
    "Foodpanda": "fa",
    "Weibo": "wi",
    "Bigo Live": "be",
    "Ace2three": "ac",
    "inpost.pl": "inp",
    "Communitygaming": "cg",
    "Rediff.com": "mrf",
    "Alfagift": "ag",
    "Shopee": "sh",
    "Fameex": "fm",
    "Blibli": "fk",
    "Ovo": "oo",
    "Gojek": "gj",
    "DANA": "dn",
    "Jingdong": "jd",
    "Badoo": "jz",
    "Snapchat": "fu",
    "alias_": "als",
    "PaxFul": "xf",
    "OfferUp": "zm",
    "Bolt": "ol",
    "Blockchain": "bc",
    "Faceit": "qz",
    "CryptoCom": "ry",
    "Dundle": "fi",
    "stripe": "je",
    "Yoshidrops": "yd",
    "KakaoTalk": "kt",
    "Kaggle": "kg",
    "Магнолия": "mn",
    "Yamaguchi": "yam",
    "УМ": "um",
    "Zoon": "zn",
    "Суточно": "sy",
    "2domains": "dom",
    "Sravni.ru": "ra",
    "Azsirbis": "az",
    "Selectel": "se",
    "Улыбка радуги": "xa",
    "РосБанк": "rb",
    "Bavarushka": "vs",
    "Едем.рф": "ed",
    "Privetmir": "pi",
    "Kvartplata.ru": "kp",
    "VseInstrumenti": "vsi",
    "Совкомбанк": "sb",
    "youdo": "ud",
    "Litnet": "et",
    "Sokolov": "sv",
    "Мой-ка": "ik",
    "Rosneft": "rn",
    "NationalLottery": "nl",
    "Leadgid.com": "lg",
    "FancyLive": "vf",
    "Trovo": "ov",
    "Сушкоф": "qx",
    "Yappy": "kj",
    "Билеты в кино": "zj",
    "Cian": "ca",
    "ЯRUS": "yr",
    "blok-post.ru": "blp",
    "Cofix": "cf",
    "Лента": "lt",
    "Solar-staff": "ss",
    "150bar": "ar",
    "СДЭК": "dk",
    "El-plat": "ep",
    "Газпром": "gp",
    "Galamart": "gal",
    "Pivko24": "pv",
    "RuVDS": "rv",
    "Hoff": "ho",
    "Xiaomi": "xi",
    "Checkin": "ci",
    "Blizzard": "bz",
    "Huya.com": "hy",
}
SERVICES = dict((v, k) for k, v in a.items())


def get_list_services(country, operator):
    url = f"https://vak-sms.com/api/getCountNumberList/?apiKey={API}&country={country}&operator={operator}&price"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.status_code)


@login_required
def get_service(request):
    if request.method == "POST":
        service = request.POST.get("service")
        url = f"https://vak-sms.com/api/getNumber/?apiKey={API}&service={service}&country=ru&operator=mts"
        services = get_list_services(country="ru", operator="mts")
        if request.user.profile.balance < int(services[service]['price']):
            return JsonResponse(
                {
                    "error": "noMoney",
                    "price": int(services[service]['price']),
                },
                content_type="application/json",
            )
        response = requests.get(url)
        price = int(services[service]["price"])
        if response.status_code == 200:
            context_service = response.json()
            print(dict(context_service).get("error"))
            if context_service.get("error"):
                return JsonResponse(
                    {
                        "error": context_service,
                        "price": price,
                    },
                    content_type="application/json",
                )
            else:
                print(context_service)
                operation = ProfileOperations(
                    profile=request.user.profile,
                    tel=context_service["tel"],
                    id_num=context_service["idNum"],
                    status="1",
                )
                operation.save()
                return JsonResponse(
                    {
                        "tel": context_service["tel"],
                        "id": context_service["idNum"],
                        "price": price,
                    },
                    content_type="application/json",
                )
        else:
            raise Exception(response.status_code)
    else:
        qr = dict(get_list_services(country="ru", operator="mts")).items()

        return render(
            request,
            "my_app/index.html",
            context={
                "services": qr,
            },
        )


def get_sms(request: HttpRequest):
    if request.method == "POST":
        id = request.POST.get("id")
        url = f"https://vak-sms.com/api/getSmsCode/?apiKey={API}&idNum={id}"
        response = requests.get(url)
        sms = response.json()
        print(sms, id)
        return JsonResponse(
            {
                "sms": sms["smsCode"],
            },
            content_type="application/json",
        )


@login_required
def popolnenie(request: HttpRequest):
    if request.method == "POST":
        new_balance = request.POST.get("money")

        profile = ProfileUser.objects.get(pk=request.user.profile.pk)
        profile.balance += int(new_balance)
        profile.save()
        return redirect("my_app:index")

    return render(request=request, template_name="my_app/popolnenie.html")


def index_page(request: HttpRequest):
    qr = dict(get_list_services(country="ru", operator="mts")).items()
    return render(
        request,
        template_name="my_app/index.html",
        context={
            "services": qr,
            "services_name": SERVICES,
        },
    )


class IndexTemplateView(TemplateView):
    template_name = "my_app/index.html"
    queryset = dict(get_list_services(country="ru", operator="mts")).items()
    extra_context = {"services": queryset}


class ShowProfile(LoginRequiredMixin, View):
    model = ProfileUser
    template_name = "my_app/profile.html"

    def get(self, request):
        user_form = request.user
        profile = ProfileUser.objects.get(user_id=user_form.pk)

        context = {
            "user_form": user_form,
            "profile": profile,
        }
        return render(
            request=request, template_name=self.template_name, context=context
        )


class EditProfile(LoginRequiredMixin, UpdateView):
    template_name = "my_app/profile_edit.html"
    model = ProfileUser
    form_class = ProfileForm

    def get_success_url(self):
        return reverse("my_app:profile")
