import requests
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import time

# ---------------------------
# Function to fetch and scrape
# ---------------------------
def scrape_books():
    BASE_URL = "http://books.toscrape.com/"
    TOTAL_PAGES = 3   # scrape first 3 pages (can be increased)
    all_books = []

    text_box.delete(1.0, tk.END)  # clear previous results
    text_box.insert(tk.END, "🔎 Starting scraping...\n")

    for page in range(1, TOTAL_PAGES + 1):
        url = f"{BASE_URL}catalogue/page-{page}.html"
        text_box.insert(tk.END, f"Fetching Page {page}: {url}\n")
        root.update()

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            products = soup.find_all("article", class_="product_pod")

            for product in products:
                name = product.h3.a["title"]
                price = product.find("p", class_="price_color").text
                availability = product.find("p", class_="instock availability").text.strip()
                all_books.append([name, price, availability])
                text_box.insert(tk.END, f"{name} | {price} | {availability}\n")

        except Exception as e:
            text_box.insert(tk.END, f"❌ Error: {e}\n")

        time.sleep(1)  # polite delay

    global scraped_data
    scraped_data = all_books
    messagebox.showinfo("Completed", f"Scraped {len(all_books)} products!")

# ---------------------------
# Function to save to CSV
# ---------------------------
def save_csv():
    if not scraped_data:
        messagebox.showwarning("No Data", "Please scrape data first!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV Files", "*.csv")])
    if file_path:
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Product Name", "Price", "Availability"])
            writer.writerows(scraped_data)
        messagebox.showinfo("Saved", f"Data saved to {file_path}")

# ---------------------------
# GUI Setup
# ---------------------------
root = tk.Tk()
root.title("Web Scraping - Product Extractor")
root.geometry("700x500")

scraped_data = []

# Buttons
frame = tk.Frame(root)
frame.pack(pady=10)

btn_scrape = tk.Button(frame, text="Scrape Data", command=scrape_books, bg="lightgreen", width=15)
btn_scrape.grid(row=0, column=0, padx=10)

btn_save = tk.Button(frame, text="Save to CSV", command=save_csv, bg="lightblue", width=15)
btn_save.grid(row=0, column=1, padx=10)

btn_exit = tk.Button(frame, text="Exit", command=root.destroy, bg="lightcoral", width=15)
btn_exit.grid(row=0, column=2, padx=10)

# Text area for results
text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
text_box.pack(pady=10)

root.mainloop()
