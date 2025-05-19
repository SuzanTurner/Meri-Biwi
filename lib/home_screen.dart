import 'package:flutter/material.dart';
import 'package:carousel_slider/carousel_slider.dart';
import 'package:home_ease/your_details.dart';
import 'package:home_ease/your_details_clean.dart'; // Assuming you have this page

class HomeScreen extends StatelessWidget {
  final List<String> topSliderImages = [
    'assets/chef/dwssc.jpg',
    'assets/chef/startupindia.jpg',
    // Add more image paths as needed
  ];

  final List<Map<String, String>> featuredServices = [
    {"title": "Domestic help", "image": "assets/chef/domestic.jpg", "route": "domestic_help"},
    {"title": "Babysitters/ Japas", "image": "assets/chef/babysitter.jpg", "route": "babysitters"},
    {"title": "Cooks", "image": "assets/chef/cook.jpg", "route": "cooks"},
    {"title": "All-rounders", "image": "assets/chef/allrounder.jpg", "route": "all_rounders"},
    {"title": "24 hrs - Full Time", "image": "assets/chef/fulltime.jpg", "route": "full_time"},
    {"title": "24 Hrs - Japas", "image": "assets/chef/japas.jpg", "route": "japas"},
  ];

  final List<Map<String, String>> exploreBroomees = [
    {
      "title": "24 Hrs - Japas",
      "subtitle": "Book your house help superhero!",
      "image": "assets/chef/japas.jpg"
    },
    // Add more if needed
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      bottomNavigationBar: BottomNavigationBar(
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home,color: Color(0xFF2E3C59)), label: "Home"),
          BottomNavigationBarItem(icon: Icon(Icons.book,color: Color(0xFF2E3C59)), label: "Bookings"),
          BottomNavigationBarItem(icon: Icon(Icons.check_circle,color: Color(0xFF2E3C59)), label: "Attendance"),
          BottomNavigationBarItem(icon: Icon(Icons.person,color: Color(0xFF2E3C59)), label: "Profile"),
        ],
      ),
      body: SafeArea(
        child: ListView(
          children: [
            // Top Location Bar
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
              child: Row(
                children: [
                  Icon(Icons.location_pin, color: Colors.orange),
                  SizedBox(width: 5),
                  Text("52CH+H3M, Dabha R...", style: TextStyle(fontWeight: FontWeight.w600)),
                  Spacer(),
                  Icon(Icons.account_circle_outlined),
                ],
              ),
            ),

            // Top Slider
            CarouselSlider(
              options: CarouselOptions(
                height: 130.0,
                autoPlay: true,
                enlargeCenterPage: true,
              ),
              items: topSliderImages.map((imgPath) {
                return Builder(
                  builder: (BuildContext context) {
                    return ClipRRect(
                      borderRadius: BorderRadius.circular(10),
                      child: Image.asset(imgPath, fit: BoxFit.cover, width: double.infinity),
                    );
                  },
                );
              }).toList(),
            ),

            // Featured Services
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text("Our featured services", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
                  SizedBox(height: 10),
                  Wrap(
                    spacing: 20,
                    runSpacing: 20,
                    children: featuredServices.map((service) {
                      return GestureDetector(
                        onTap: () {
                          if (service["title"] == "Domestic help") {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => YourDetailsClean(),
                              ),
                            );
                          } else {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => YourDetails(),
                              ),
                            );
                          }
                        },
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            CircleAvatar(
                              radius: 35,
                              backgroundImage: AssetImage(service["image"]!),
                            ),
                            SizedBox(height: 5),
                            SizedBox(
                              width: 80,
                              child: Text(
                                service["title"]!,
                                textAlign: TextAlign.center,
                                style: TextStyle(fontSize: 12),
                              ),
                            ),
                          ],
                        ),
                      );
                    }).toList(),
                  ),
                ],
              ),
            ),

            // Explore Broomees
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: Text("Explore Broomees", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            ),
            SizedBox(height: 10),
            CarouselSlider(
              options: CarouselOptions(
                height: 200.0,
                autoPlay: true,
                enlargeCenterPage: true,
              ),
              items: exploreBroomees.map((item) {
                return Builder(
                  builder: (BuildContext context) {
                    return Container(
                      margin: EdgeInsets.symmetric(horizontal: 5),
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(15),
                        image: DecorationImage(
                          image: AssetImage(item["image"]!),
                          fit: BoxFit.cover,
                        ),
                      ),
                      child: Container(
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(15),
                          color: Colors.black.withOpacity(0.4),
                        ),
                        padding: EdgeInsets.all(16),
                        child: Align(
                          alignment: Alignment.bottomLeft,
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(item["title"]!, style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
                              SizedBox(height: 5),
                              Text(item["subtitle"]!, style: TextStyle(color: Colors.white, fontSize: 12)),
                              SizedBox(height: 10),
                              ElevatedButton(
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: Colors.amber,
                                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                                ),
                                onPressed: () {},
                                child: Text("Book Now!"),
                              ),
                            ],
                          ),
                        ),
                      ),
                    );
                  },
                );
              }).toList(),
            ),
          ],
        ),
      ),
    );
  }
}