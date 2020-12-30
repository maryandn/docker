import xml.dom.minidom
import requests
import json
from datetime import date, timedelta


def main():
    try:
        doc = xml.dom.minidom.parse('epg-all.xml')
        url_channels = 'http://app:8000/channels/get_channels/'
        url_programmes = 'http://app:8000/channels/get_programmes/'
        headers = {'Content-Type': 'application/json'}
        default_list_channels = []
        default_list_programmes = []

        channels = doc.getElementsByTagName("channel")
        for channel in channels:
            default_dict_channel = {}
            id = channel.getAttribute('id')
            default_dict_channel.update({"id": id})
            displayName = channel.getElementsByTagName("display-name")[0]
            default_dict_channel.update({"name": displayName.firstChild.data})
            lang = displayName.getAttribute('lang')
            default_dict_channel.update({"lang": lang})

            default_list_channels.append(default_dict_channel)

        data_channels = json.dumps(default_list_channels)
        requests.post(url_channels, data=data_channels, headers=headers)

        programmes = doc.getElementsByTagName("programme")
        for programme in programmes:
            default_dict_programme = {}
            channel_id = programme.getAttribute('channel')
            default_dict_programme.update({'channel_id': channel_id})
            start_programme = programme.getAttribute('start')
            stop_programme = programme.getAttribute('stop')
            title = programme.getElementsByTagName("title")[0].firstChild.data
            # desc = programme.getElementsByTagName("desc")
            # if len(desc) > 0:
            #     desc = desc[0].firstChild.data
            # else:
            #     desc = ""
            default_dict_programme.update({'start': start_programme})
            default_dict_programme.update({'stop': stop_programme})
            default_dict_programme.update({'title': title})
            default_dict_programme.update({'description': ''})
            default_list_programmes.append(default_dict_programme)

        data_programmes = json.dumps(default_list_programmes)
        requests.post(url_programmes, data=data_programmes, headers=headers)
    except Exception as err:
        print(err)

main()
# def get_from_api(filename):
#     try:
#         default_ch_list = []
#         doc = xml.dom.minidom.Document()
#         root = doc.createElement("tv")
#         root.setAttribute('generator-info-name', 'EPG')
#         doc.appendChild(root)
#
#         res = requests.get('http://127.0.0.1:8000/channels/get_for_file/ch/1U530oiglQ').json()
#
#         for i in res:
#             default_ch_list.append(i['id'])
#             channel = doc.createElement("channel")
#             channel.setAttribute('id', str(i['id']))
#
#             display_name = doc.createElement('display-name')
#             display_name_text = doc.createTextNode(str(i['name']))
#             display_name.appendChild(display_name_text)
#             display_name.setAttribute('lang', str(i['lang']))
#             channel.appendChild(display_name)
#
#             root.appendChild(channel)
#
#         for ch in default_ch_list:
#             all_pr = requests.get(f"http://127.0.0.1:8000/channels/get_for_file/pr/1U530oiglQ/{ch}").json()
#             for pr in all_pr:
#                 programme = doc.createElement('programme')
#                 programme.setAttribute('start', str(pr['start']))
#                 programme.setAttribute('stop', str(pr['stop']))
#                 programme.setAttribute('channel', str(pr['channel_id']))
#                 title = doc.createElement('title')
#                 title.setAttribute('lang', 'ru')
#                 title_text = doc.createTextNode(str(pr['title']))
#                 title.appendChild(title_text)
#                 # desc = doc.createElement('desc')
#                 # desc.setAttribute('lang', 'ru')
#                 # desc_text = doc.createTextNode(str(pr['description']))
#                 # desc.appendChild(desc_text)
#
#                 programme.appendChild(title)
#                 # programme.appendChild(desc)
#
#                 root.appendChild(programme)
#
#         xml_str = doc.toprettyxml(indent="  ", encoding="utf-8")
#         with open(filename, "wb") as f:
#             f.write(xml_str)
#     except Exception as err:
#         print(err)
#
#
# if __name__ == "__main__":
#     get_from_api("app-res.xml")

# def get_all_api(filename):
#     try:
#         doc = xml.dom.minidom.Document()
#         root = doc.createElement("tv")
#         root.setAttribute('generator-info-name', 'EPG')
#         doc.appendChild(root)
#
#         res = requests.get(f"http://app:8000/channels/get_for_file/{filename['token']}").json()
#
#         for i in res['channels']:
#             channel = doc.createElement("channel")
#             channel.setAttribute('id', str(i['id']))
#
#             display_name = doc.createElement('display-name')
#             display_name_text = doc.createTextNode(str(i['name']))
#             display_name.appendChild(display_name_text)
#             display_name.setAttribute('lang', str(i['lang']))
#             channel.appendChild(display_name)
#
#             root.appendChild(channel)
#
#         for p in res['programme']:
#             programme = doc.createElement('programme')
#             programme.setAttribute('start', str(p['start']))
#             programme.setAttribute('stop', str(p['stop']))
#             programme.setAttribute('channel', str(p['channel_id']))
#             title = doc.createElement('title')
#             title.setAttribute('lang', 'ru')
#             title_text = doc.createTextNode(str(p['title']))
#             title.appendChild(title_text)
#
#             programme.appendChild(title)
#
#             root.appendChild(programme)
#
#         xml_str = doc.toprettyxml(indent="  ", encoding="utf-8")
#         with open(filename['name_service'] + ".xml", "wb") as f:
#             f.write(xml_str)
#
#     except Exception as err:
#         print(err)
#
#
# def list_provider():
#     main()
#     list_prov = requests.get('http://app:8000/channels/get_token_list').json()
#     for provider in list_prov:
#         get_all_api(provider)
#     req_del = requests.delete(f"http://app:8000/channels/del_day?day={date.today() - timedelta(days=14)}").json()
#     print('Done generate new file and', req_del['msg'])
#
#
# if __name__ == "__main__":
#     list_provider()
