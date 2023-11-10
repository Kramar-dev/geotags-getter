import os
import exifread


class Geotag:
    pics_extensions = ('.jpg', '.jpeg', '.png', '.gif')

    @staticmethod
    def get(directory):
        for root, dirs, files in os.walk(directory):
            root = root.replace('\\', '/')
            print(root)
            for filename in files:
                if filename.lower().endswith(Geotag.pics_extensions):
                    image_path = os.path.join(root, filename)
                    location = Geotag.__extract_location_from_image(image_path)
                    if location:
                        print(f"\t{filename} {str(location[0])}, {str(location[1])}")

    @staticmethod
    def __convert_dms_to_decimal(dms):
        degrees, minutes, seconds = [float(x.num) / float(x.den) for x in dms]
        return degrees + (minutes / 60) + (seconds / 3600)

    @staticmethod
    def __extract_location_from_image(image_path):
        with open(image_path, 'rb') as image_file:
            tags = exifread.process_file(image_file)

        if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
            latitude_dms = tags['GPS GPSLatitude'].values
            longitude_dms = tags['GPS GPSLongitude'].values

            latitude = Geotag.__convert_dms_to_decimal(latitude_dms)
            longitude = Geotag.__convert_dms_to_decimal(longitude_dms)

            if tags['GPS GPSLatitudeRef'] == 'S':
                latitude = -latitude
            if tags['GPS GPSLongitudeRef'] == 'W':
                longitude = -longitude

            return latitude, longitude
        return None


if __name__ == '__main__':
    photo_directory = "path/to/pictures"
    Geotag.get(photo_directory)
