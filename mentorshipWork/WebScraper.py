import requests
from bs4 import BeautifulSoup as bs
import re
import csv
import shutil

f = r"C:\Users\jkang\Documents\mentorshipWork\GeoJson.csv"
rows = []
page = 0
while page != 5:
      url_salb1 = f"https://salb.un.org/en/data?title=&field_un_region_target_id=All&page={page}"

      salb_page1 = requests.get(url_salb1)

      salb_soup1 = bs(salb_page1.content, "html.parser")
      salb_results1 = salb_soup1.find(id="block-un2-theme-content")

      
      salb_data1 = salb_results1.find_all("tr")
      for salb_x in salb_data1:
        data =[]
        salb_name_element = salb_x.find("a")
        salb_set_elements = salb_x.find("span", class_="text-muted")
        
        
        salb_n = str(salb_name_element)[23:-4]
        salb_ref = str(salb_name_element)[9:21]
        salb_s = str(salb_set_elements)[25:29]
        salb_cc = str(salb_ref)[9:13]
        
        
        data.append(salb_n)
        data.append(salb_cc)
      
        
        url_salb2 = f"https://salb.un.org{salb_ref}"
        salb_page2 = requests.get(url_salb2)

        salb_soup2 = bs(salb_page2.content, "html.parser")
        salb_results2 = salb_soup2.find(id="block-un2-theme-content", class_="block block-system block-system-main-block")

        salb_data2 = salb_results2.find_all("div", class_="field field--name-title field--type-string field--label-hidden field__item pattern-field variant- size-normal font-color-normal")
        salb_data2_1 = salb_results2.find_all("li", class_="list-group-item")
        

        for salb_y in salb_data2:
          salb_dept_element = salb_y.find("h4")

          salb_dept = str(salb_dept_element)[4:-5]

          data.append(salb_dept)

        if salb_s != "None":
          data.append(url_salb2)
        
        a=0
        for salb_y1 in salb_data2_1:
          if a >= 1: continue
          salb_geojson_label = salb_y1.find(string=re.compile("GeoJson"))
          salb_geojson_list = salb_geojson_label.find_parents("a")
          
          for result in salb_geojson_list:
            salb_geojson = result['href']
            data.append(salb_geojson)
            response = requests.get(salb_geojson)
            open(salb_n + ".geojson", "wb").write(response.content)
            
            current_loc = salb_n + ".geojson"
            new_loc = r"C:\\Users\\jkang\Documents\\mentorshipWork\\Geojsons\\" + current_loc
            shutil.move(current_loc, new_loc)
            a += 1
            

        

        print()
        print(data)
        rows.append(data)
        with open(f, 'w', encoding="utf-8") as csvfile:
          csvwriter = csv.writer(csvfile)
          csvwriter.writerows(rows)
     
      
      

      
      page = page + 1
