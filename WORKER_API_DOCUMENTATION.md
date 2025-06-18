# Worker API Documentation - Multipart Form Data

## Overview
The Worker API endpoints have been updated to use multipart form data instead of JSON. This allows for file uploads along with form data in a single request.

## Endpoints

### 1. Register Worker (POST /workers/)
**Content-Type:** `multipart/form-data`

#### Required Fields:
- `full_name` (string): Worker's full name
- `gender` (string): Worker's gender
- `age` (integer): Worker's age
- `dob` (string): Date of birth
- `phone` (string): Phone number
- `email` (string): Email address
- `city` (string): City
- `primary_service_category` (string): Primary service category
- `experience_years` (integer): Years of experience
- `experience_months` (integer): Months of experience
- `languages_spoken` (string): JSON array of languages
- `availability` (string): JSON array of availability
- `preferred_community` (string): JSON array of preferred communities
- `aadhar_number` (string): Aadhar number
- `pan_number` (string): PAN number

#### Optional Fields:
- `alternate_phone` (string): Alternate phone number
- `blood_group` (string): Blood group
- `status` (string): Status (default: "Pending")
- `religion` (string): Religion (default: "God knows")

#### File Uploads:
- `profile_photo` (file): Profile photo
- `electricity_bill` (file): Electricity bill document
- `live_capture` (file): Live capture photo
- `photoshoot` (file): Photoshoot photo

#### Nested Data (JSON strings):
- `permanent_address` (string): JSON object for permanent address
- `current_address` (string): JSON object for current address
- `emergency_contacts` (string): JSON array of emergency contacts
- `bank_details` (string): JSON object for bank details
- `police_verification` (string): JSON object for police verification
- `local_references` (string): JSON array of local references
- `previous_employers` (string): JSON array of previous employers
- `education` (string): JSON array of education records

### 2. Get All Workers (GET /workers/)
Returns a list of all workers with basic information.

### 3. Get Worker Details (GET /workers/{worker_id}/details)
Returns complete worker information including all related data (addresses, contacts, references, etc.).

### 4. Update Worker (PUT /workers/{worker_id})
**Content-Type:** `multipart/form-data`

**All fields are optional for updates.** Only provide the fields you want to update. This endpoint can edit ALL parameters available for a worker, including individual fields within related tables.

#### Basic Worker Information:
- `full_name`, `gender`, `age`, `dob`, `phone`, `alternate_phone`, `email`, `city`, `blood_group`
- `primary_service_category`, `experience_years`, `experience_months`
- `languages_spoken`, `availability`, `preferred_community` (JSON strings)
- `aadhar_number`, `pan_number`, `status`, `religion`

#### File Uploads:
- `profile_photo`, `electricity_bill`, `live_capture`, `photoshoot`

#### Individual Address Fields:
**Permanent Address:**
- `permanent_address_line1`, `permanent_address_city`, `permanent_address_state`, `permanent_address_zip_code`

**Current Address:**
- `current_address_line1`, `current_address_city`, `current_address_state`, `current_address_zip_code`

#### Individual Bank Details Fields:
- `bank_ifsc_code`, `bank_account_number`, `bank_name`

#### Individual Police Verification Fields:
- `police_status`, `police_document_url`, `police_verification_date`, `police_remarks`

#### Related Data (JSON arrays for multiple records):
- `emergency_contacts` (JSON string) - Replace entire list
- `local_references` (JSON string) - Replace entire list  
- `previous_employers` (JSON string) - Replace entire list
- `education` (JSON string) - Replace entire list

### 5. Search Workers (GET /workers/{name})
Search workers by name.

### 6. Delete Worker (DELETE /workers/{id})
Delete a worker by ID.

## JSON Format Examples

### Languages Spoken
```json
["English", "Hindi", "Marathi"]
```

### Availability
```json
["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
```

### Preferred Community
```json
["Local", "Religious"]
```

### Permanent Address
```json
{
  "line1": "123 Main Street",
  "city": "Mumbai",
  "state": "Maharashtra",
  "zip_code": "400001"
}
```

### Current Address
```json
{
  "line1": "456 Current Street",
  "city": "Mumbai",
  "state": "Maharashtra",
  "zip_code": "400002"
}
```

### Emergency Contacts
```json
[
  {
    "name": "John Doe",
    "relation": "Father",
    "phone": "9876543210"
  },
  {
    "name": "Jane Doe",
    "relation": "Mother",
    "phone": "9876543211"
  }
]
```

### Bank Details
```json
{
  "ifsc_code": "SBIN0001234",
  "account_number": "1234567890",
  "bank_name": "State Bank of India"
}
```

### Police Verification
```json
{
  "status": "Verified",
  "document_url": "https://example.com/document.pdf",
  "verification_date": "2024-01-15",
  "remarks": "All documents verified"
}
```

### Local References
```json
[
  {
    "name": "Reference 1",
    "relation": "Neighbor",
    "phone": "9876543212"
  },
  {
    "name": "Reference 2",
    "relation": "Friend",
    "phone": "9876543213"
  }
]
```

### Previous Employers
```json
[
  {
    "company_name": "ABC Company",
    "position": "Housekeeper",
    "duration": "2 years"
  },
  {
    "company_name": "XYZ Services",
    "position": "Cook",
    "duration": "1 year"
  }
]
```

### Education
```json
[
  {
    "degree": "High School",
    "institution": "ABC School",
    "year_of_passing": "2015"
  },
  {
    "degree": "Diploma in Housekeeping",
    "institution": "DEF Institute",
    "year_of_passing": "2016"
  }
]
```

## Example cURL Requests

### Register Worker
```bash
curl -X POST "http://localhost:8000/workers/" \
  -H "Content-Type: multipart/form-data" \
  -F "full_name=John Doe" \
  -F "gender=Male" \
  -F "age=25" \
  -F "dob=1999-01-01" \
  -F "phone=9876543210" \
  -F "email=john@example.com" \
  -F "city=Mumbai" \
  -F "primary_service_category=cleaning" \
  -F "experience_years=2" \
  -F "experience_months=6" \
  -F "languages_spoken=[\"English\", \"Hindi\"]" \
  -F "availability=[\"Monday\", \"Tuesday\", \"Wednesday\"]" \
  -F "preferred_community=[\"Local\"]" \
  -F "aadhar_number=123456789012" \
  -F "pan_number=ABCDE1234F" \
  -F "profile_photo=@/path/to/photo.jpg" \
  -F "electricity_bill=@/path/to/bill.pdf" \
  -F "permanent_address={\"line1\":\"123 Main St\",\"city\":\"Mumbai\",\"state\":\"Maharashtra\",\"zip_code\":\"400001\"}" \
  -F "emergency_contacts=[{\"name\":\"Jane Doe\",\"relation\":\"Wife\",\"phone\":\"9876543211\"}]"
```

### Update Worker (Individual Fields)
```bash
# Update basic worker info
curl -X PUT "http://localhost:8000/workers/1" \
  -H "Content-Type: multipart/form-data" \
  -F "full_name=John Smith" \
  -F "age=26"

# Update individual address fields
curl -X PUT "http://localhost:8000/workers/1" \
  -H "Content-Type: multipart/form-data" \
  -F "permanent_address_city=Mumbai" \
  -F "permanent_address_zip_code=400002"

# Update individual bank details
curl -X PUT "http://localhost:8000/workers/1" \
  -H "Content-Type: multipart/form-data" \
  -F "bank_ifsc_code=SBIN0001234" \
  -F "bank_account_number=1234567890"

# Update individual police verification
curl -X PUT "http://localhost:8000/workers/1" \
  -H "Content-Type: multipart/form-data" \
  -F "police_status=Verified" \
  -F "police_verification_date=2024-01-15"

# Update emergency contacts (replace entire list)
curl -X PUT "http://localhost:8000/workers/1" \
  -H "Content-Type: multipart/form-data" \
  -F "emergency_contacts=[{\"name\":\"Jane Smith\",\"relation\":\"Wife\",\"phone\":\"9876543211\"}]"
```

### Get Worker Details
```bash
curl -X GET "http://localhost:8000/workers/1/details"
```

## Notes
- All JSON strings must be properly escaped when sent as form data
- File uploads are optional
- Individual field updates are supported for addresses, bank details, and police verification
- For arrays (emergency contacts, references, employers, education), you must provide the complete JSON array to replace the existing data
- The API will validate JSON format and return appropriate error messages for invalid JSON
- File uploads are saved with unique timestamps to prevent conflicts
- The PUT endpoint supports partial updates - only send the fields you want to change
- All relationships (addresses, contacts, references, employers, education, bank details, police verification) are properly handled in both POST and PUT endpoints
- Individual field updates will create new records if they don't exist, or update existing records if they do exist
- **JSON Field Handling**: If you send simple strings like "string" instead of valid JSON, the API will treat them as empty/default values
- **Required JSON Fields**: For POST requests, `languages_spoken`, `availability`, and `preferred_community` must be valid JSON arrays (even if empty like `[]`)

## Common Issues and Solutions

### Issue: "Invalid JSON format" error
**Cause**: Sending simple strings instead of valid JSON for complex fields
**Solution**: Use proper JSON format

**❌ Wrong:**
```
-F 'languages_spoken=string'
-F 'emergency_contacts=string'
```

**✅ Correct:**
```
-F 'languages_spoken=["English", "Hindi"]'
-F 'emergency_contacts=[{"name":"John","relation":"Father","phone":"1234567890"}]'
```

### Issue: Empty arrays/objects
**Solution**: Use empty JSON arrays/objects

**✅ Correct:**
```
-F 'languages_spoken=[]'
-F 'emergency_contacts=[]'
-F 'permanent_address={}'
```

### Issue: Special characters in JSON
**Solution**: Properly escape quotes and special characters

**✅ Correct:**
```
-F 'emergency_contacts=[{\"name\":\"John Doe\",\"relation\":\"Father\",\"phone\":\"1234567890\"}]'
``` 