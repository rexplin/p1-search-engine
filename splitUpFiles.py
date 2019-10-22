import json


if __name__ == "__main__":
    with open('wikipedia_data_lines.json', 'r') as in_json_file:
        for json_obj in in_json_file:
            json_datas = json.loads(json_obj)
            filename = f"../wiki-files-separated/file{int((json_datas['id'])/200000)+1}/wiki-doc-{json_datas['id']}.json"
            with open(filename, 'w') as out_json_file:
                json.dump(json_datas, out_json_file)
