import requests
from bs4 import BeautifulSoup
import time

def scrape_internships(job_type, category, min_jobs=6):
    # Base URL for Internshala
    if job_type.lower() == "internship":
        # Map category to Internshala's URL-friendly format
        category_map = {
            "python": "python%2Fdjango-internship",
            "aiml": "machine-learning-internship",
            "web development": "web-development-internship",
            "data science": "data-science-internship",
            "other": "internships"
        }
        category_url = category_map.get(category.lower(), "internships")
        base_url = f"https://internshala.com/{category_url}"
    elif job_type.lower() == "parttime":
        base_url = f"https://internshala.com/internships/part-time-jobs"
    else:  # fulltime
        base_url = f"https://internshala.com/jobs/"

    try:
        # Send HTTP request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()  # Check for request errors
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find job listings (Internshala's job/internship card class)
        job_listings = soup.find_all("div", class_="internship_meta")
        
        if not job_listings:
            print(f"No {job_type} found for category '{category}' on Internshala.")
            return
        
        # Process and display job listings
        print(f"\n=== {job_type.capitalize()} in {category.capitalize()} from Internshala ===")
        count = 0
        for job in job_listings:
            if count >= min_jobs:  # Stop after scraping at least 6 jobs
                break
            
            title = job.find("h3", class_="heading_4_5 profile")
            company = job.find("a", class_="link_display_like_text")
            location = job.find("a", class_="location_link")  # Fixed: Added closing quote and parenthesis
            link = job.find("a", class_="view_detail_button", href=True)
            
            # Extract text or set defaults if not found
            title_text = title.text.strip() if title else "N/A"
            company_text = company.text.strip() if company else "N/A"
            location_text = location.text.strip() if location else "N/A"
            job_url = f"https://internshala.com{link['href']}" if link else "N/A"
            
            print(f"Internship {count + 1}:")
            print(f"Title: {title_text}")
            print(f"Company: {company_text}")
            print(f"Location: {location_text}")
            print(f"URL: {job_url}")
            print("-" * 50)
            
            count += 1
        
        if count < min_jobs:
            print(f"Note: Only {count} internships found (less than requested {min_jobs}).")
        
    except requests.RequestException as e:
        print(f"Error fetching internships from Internshala: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    print("Welcome to the Internshala Internship Scraper Demo!")
    print("This is a project demo to scrape internships from Internshala.")
    
    # Job type selection
    print("\nChoose a job type:")
    print("1. Full-time")
    print("2. Internship")
    print("3. Part-time")
    job_choice = input("Enter your choice (1-3): ")
    
    job_types = {
        "1": "fulltime",
        "2": "internship",
        "3": "parttime"
    }
    selected_job_type = job_types.get(job_choice, "internship")  # Default to internship
    
    # Category selection
    print("\nChoose a job category:")
    print("1. Python")
    print("2. AI/ML")
    print("3. Web Development")
    print("4. Data Science")
    print("5. Other")
    category_choice = input("Enter your choice (1-5): ")
    
    category_map = {
        "1": "python",
        "2": "aiml",
        "3": "web development",
        "4": "data science",
        "5": "other"
    }
    selected_category = category_map.get(category_choice, "other")
    
    print(f"\nScraping {selected_job_type} in {selected_category} from Internshala...")
    scrape_internships(selected_job_type, selected_category)

if __name__ == "__main__":
    main()