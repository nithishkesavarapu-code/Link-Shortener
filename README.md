# LinkTrim: Scalable URL Shortener with Analytics

**LinkTrim** is a full-stack URL shortening service that focuses on **system design efficiency** and **data observability**. It features a custom shortening algorithm and a built-in dashboard to visualize click-stream data, demonstrating the ability to handle data-intensive applications.

## 🚀 Key Features
* **URL Shortening:** Converts long URLs into 5-character unique alphanumeric codes using `ShortUUID`.
* **Instant Redirection:** Low-latency lookup and redirection.
* **Analytics Dashboard:** Visualizes traffic data, including total clicks and timestamps.
* **Data Persistence:** Uses SQLite for reliable storage of link mapping and click logs.
<img width="1919" height="916" alt="image" src="https://github.com/user-attachments/assets/c13f2751-980c-4c64-a675-5c9ad12b9d06" />
<img width="1919" height="914" alt="image" src="https://github.com/user-attachments/assets/13747ae0-dd64-4a91-b0ff-4ed313f84322" />


## 🛠️ Tech Stack
* **Backend:** Python (Flask)
* **Database:** SQLite (Relational Data Model)
* **Templating:** Jinja2
* **Utilities:** ShortUUID

## ⚙️ Database Schema
The project uses a relational model to ensure data integrity:
1.  **Table `urls`:** Stores `original_url`, `short_code`, and `created_at`.
2.  **Table `clicks`:** Stores access logs (`short_code`, `click_time`, `user_agent`) to enable granular analytics.

## 🏃‍♂️ How to Run locally

### Prerequisites
* Python 3.8+

### Installation
1.  Clone the repository:
   
2.  Install dependencies:
    ```bash
    pip install flask shortuuid
    ```
3.  Start the application:
    ```bash
    python app.py
    ```
4.  Access the App:
    * **Shortener:** `http://localhost:5000`
    * **Dashboard:** `http://localhost:5000/dashboard`

## 🔮 Future Improvements
* **Caching:** Implement **Redis** to cache hot URLs and reduce database reads (Read-heavy system optimization).
* **Containerization:** Add `Dockerfile` for easy deployment to cloud services.
* **Rate Limiting:** Prevent API abuse using Flask-Limiter.
