import requests
from bs4 import BeautifulSoup
import streamlit as st

def translate_company_name(name_vn: str) -> str:
    name_en = name_vn
    name_en = name_en.replace("CÔNG TY TNHH", "Co Ltd")
    name_en = name_en.replace("Công Ty TNHH", "Co Ltd")
    name_en = name_en.replace("CÔNG TY CP", "JSC")
    name_en = name_en.replace("Công Ty CP", "JSC")
    return name_en

def get_company_info(tax_code: str):
    url = f"https://masothue.com/{tax_code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    company_name = soup.find("h1").get_text(strip=True)
    company_name_en = translate_company_name(company_name)

    info_table = soup.find("table", class_="table-taxinfo")
    info = {}
    if info_table:
        rows = info_table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 2:
                key = cols[0].get_text(strip=True)
                value = cols[1].get_text(strip=True)
                info[key] = value
    
    return company_name, company_name_en, info

st.title("Tra cứu thông tin doanh nghiệp từ mã số thuế")

tax_code = st.text_input("Nhập mã số thuế:", "")

if tax_code:
    result = get_company_info(tax_code)
    if result:
        company_name, company_name_en, info = result
        st.subheader("Thông tin công ty (Tiếng Việt)")
        st.write(f"**Tên công ty:** {company_name}")
        for k, v in info.items():
            st.write(f"**{k}:** {v}")

        st.subheader("Company Information (English)")
        st.write(f"**Company Name:** {company_name_en}")
        if "Địa chỉ" in info:
            st.write(f"**Address:** {info['Địa chỉ']}")
        if "Người đại diện" in info:
            st.write(f"**Legal Representative:** {info['Người đại diện']}")
        if "Điện thoại" in info:
            st.write(f"**Phone:** {info['Điện thoại']}")
    else:
        st.error("Không thể truy cập trang web hoặc mã số thuế không hợp lệ.")
