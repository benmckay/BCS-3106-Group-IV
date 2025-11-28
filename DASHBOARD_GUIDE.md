# Construction Intelligence Dashboard Guide

## Overview
This guide covers the analytics dashboard available at `/api/dashboard/`. The dashboard surfaces operational metrics, interactive Matplotlib charts, and export options without requiring any additional frontend framework. Charts and reports are generated server-side to ensure consistent styling and accuracy.

## Features
- Live statistics cards for jobs, estimates, invoices, and revenue
- Worker availability, material spend, average job duration, and customer satisfaction insights
- Nine Matplotlib charts grouped into Overview, Financial, Workforce, and Performance tabs
- Auto-refresh every five minutes plus manual refresh control
- Recent activity feed combining jobs and invoices
- Export options for PDF and Excel, each embedding charts and summary metrics

## Setup
1. Install dependencies:
   - `pip install -r requirements.txt`
2. Apply migrations and start the server:
   - `python manage.py migrate`
   - `python manage.py runserver`
3. Visit `http://localhost:8000/api/dashboard/` in a browser.
4. Authenticate via API or Django admin before using the data endpoints.

## API Endpoints
| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/dashboard/` | GET | Renders the HTML dashboard |
| `/api/dashboard-stats/` | GET | Returns aggregated metrics used by the stats cards |
| `/api/dashboard-charts/` | GET | Returns base64-encoded PNG charts |
| `/api/export-dashboard/?format=pdf` | GET | Generates a landscape PDF report |
| `/api/export-dashboard/?format=excel` | GET | Generates a multi-sheet Excel workbook |

All API endpoints except `/api/dashboard/` require authentication via JWT or session cookies.

## Export Formats
### PDF
- Landscape A4 layout with hero title, timestamp, and summary metrics
- Charts arranged two per page, preserving aspect ratio

### Excel
- `Summary` sheet containing key metrics
- `Recent Activity` sheet with the latest jobs and invoices
- Dedicated sheet per chart with embedded PNG and title heading

## Troubleshooting
| Symptom | Resolution |
| --- | --- |
| Charts missing | Ensure Matplotlib and Pillow are installed; restart the server after installing dependencies |
| Export downloads fail | Confirm `reportlab` and `openpyxl` are installed and the process has file-write permissions |
| Empty statistics | Seed the database with customers, jobs, invoices, and materials |
| Unauthorized errors | Authenticate first or include a valid JWT in the `Authorization` header |

## Future Enhancements
- Custom date filters for charts and exports
- CSV export option for raw data
- WebSocket push updates for near real-time monitoring
- Role-based widgets tailored to finance or operations teams
