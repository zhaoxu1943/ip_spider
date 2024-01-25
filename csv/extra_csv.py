import csv
import json

asn_obj_map = {}
asn_list = []


class ASN:
    def __init__(self, name, count, sum):
        self.name = name
        self.count = count
        self.sum = sum

    def __eq__(self, other):
        if isinstance(other, ASN):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)


def test():
    # Read the file
    with open('/home/ip_asn.txt', 'r', encoding="UTF-8") as file:
        data = file.readlines()

    for line in data:
        json_data = json.loads(line)
        asn_description = json_data.get('asn_description')
        if asn_description in asn_obj_map:
            temp_asn_obj = asn_obj_map.get(asn_description)
            temp_asn_obj.count += 1
            temp_sum = int(json_data.get('maxip')) - int(json_data.get('minip'))
            temp_asn_obj.sum += temp_sum
        else:
            temp_sum = int(json_data.get('maxip')) - int(json_data.get('minip'))
            temp_asn_obj = ASN(asn_description, 1, temp_sum)
            asn_obj_map[asn_description] = temp_asn_obj

    for asn_obj in asn_obj_map.values():
        asn_list.append(asn_obj)

    asn_list.sort(key=lambda x: x.count, reverse=True)

    filename = '/home/output_2.csv'
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Count', 'Sum'])
        for asn_obj in asn_list:
            writer.writerow([asn_obj.name, asn_obj.count, asn_obj.sum])


if __name__ == '__main__':
    test()
