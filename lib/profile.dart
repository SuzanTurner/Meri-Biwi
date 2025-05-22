import 'package:flutter/material.dart';

class UserProfilesPage extends StatefulWidget {
  @override
  _UserProfilesPageState createState() => _UserProfilesPageState();
}

class _UserProfilesPageState extends State<UserProfilesPage> {
  bool _darkModeEnabled = true; // Initial state for dark mode

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Profile'),
        backgroundColor: Colors.grey[900], // Match the dark background
      ),
      backgroundColor: Colors.grey[900], // Match the dark background
      body: ListView(
        padding: EdgeInsets.all(16.0),
        children: <Widget>[
          Row(
            children: <Widget>[
              CircleAvatar(
                radius: 30,
                backgroundColor: Colors.grey[800],
                child: Icon(
                  Icons.person,
                  size: 40,
                  color: Colors.white,
                ),
              ),
              SizedBox(width: 16.0),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  Text(
                    'Hello! Guest',
                    style: TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                      fontSize: 18.0,
                    ),
                  ),
                  Text(
                    'Login or signup',
                    style: TextStyle(
                      color: Colors.grey[400],
                      fontSize: 14.0,
                    ),
                  ),
                ],
              ),
            ],
          ),
          SizedBox(height: 24.0),
          Text(
            'Preferences',
            style: TextStyle(
              color: Colors.grey[400],
              fontWeight: FontWeight.bold,
              fontSize: 16.0,
            ),
          ),
          Divider(color: Colors.grey[800], height: 20.0, thickness: 1.0),
          ListTile(
            leading: Icon(Icons.language, color: Colors.blue[300]),
            title: Text('Language', style: TextStyle(color: Colors.white)),
            trailing: Text('English', style: TextStyle(color: Colors.grey[400])),
          ),
          ListTile(
            leading: Icon(Icons.brightness_2, color: Colors.blue[300]),
            title: Text('Dark Mode', style: TextStyle(color: Colors.white)),
            trailing: Switch(
              value: _darkModeEnabled,
              onChanged: (bool value) {
                setState(() {
                  _darkModeEnabled = value;
                  // You would typically trigger a theme change here
                  print('Dark mode is now ${_darkModeEnabled ? 'on' : 'off'}');
                });
              },
              activeColor: Colors.greenAccent,
              inactiveTrackColor: Colors.grey[600],
            ),
          ),
          SizedBox(height: 24.0),
          Text(
            'Legal',
            style: TextStyle(
              color: Colors.grey[400],
              fontWeight: FontWeight.bold,
              fontSize: 16.0,
            ),
          ),
          Divider(color: Colors.grey[800], height: 20.0, thickness: 1.0),
          ListTile(
            leading: Icon(Icons.description, color: Colors.blue[300]),
            title: Text('Terms & conditions', style: TextStyle(color: Colors.white)),
            trailing: Icon(Icons.arrow_forward_ios, color: Colors.grey[400], size: 16.0),
            onTap: () {
              // Handle tap
            },
          ),
          ListTile(
            leading: Icon(Icons.security, color: Colors.blue[300]),
            title: Text('Privacy Policy', style: TextStyle(color: Colors.white)),
            trailing: Icon(Icons.arrow_forward_ios, color: Colors.grey[400], size: 16.0),
            onTap: () {
              // Handle tap
            },
          ),
          SizedBox(height: 24.0),
          Text(
            'Others',
            style: TextStyle(
              color: Colors.grey[400],
              fontWeight: FontWeight.bold,
              fontSize: 16.0,
            ),
          ),
          Divider(color: Colors.grey[800], height: 20.0, thickness: 1.0),
          ListTile(
            leading: Icon(Icons.group_add, color: Colors.blue[300]),
            title: Text('Provider', style: TextStyle(color: Colors.white)),
            trailing: Icon(Icons.arrow_forward_ios, color: Colors.grey[400], size: 16.0),
            onTap: () {
              // Handle tap
            },
          ),
          ListTile(
            leading: Icon(Icons.share, color: Colors.blue[300]),
            title: Text('Share App', style: TextStyle(color: Colors.white)),
            trailing: Icon(Icons.arrow_forward_ios, color: Colors.grey[400], size: 16.0),
            onTap: () {
              // Handle tap
            },
          ),
          ListTile(
            leading: Icon(Icons.star_border, color: Colors.blue[300]),
            title: Text('Rate App', style: TextStyle(color: Colors.white)),
            trailing: Icon(Icons.arrow_forward_ios, color: Colors.grey[400], size: 16.0),
            onTap: () {
              // Handle tap
            },
          ),
          ListTile(
            leading: Icon(Icons.question_mark, color: Colors.blue[300]),
            title: Text('FAQs', style: TextStyle(color: Colors.white)),
            trailing: Icon(Icons.arrow_forward_ios, color: Colors.grey[400], size: 16.0),
            onTap: () {
              // Handle tap
            },
          ),
          ListTile(
            leading: Icon(Icons.phone, color: Colors.blue[300]),
            title: Text('Contact Us', style: TextStyle(color: Colors.white)),
            trailing: Icon(Icons.arrow_forward_ios, color: Colors.grey[400], size: 16.0),
            onTap: () {
              // Handle tap
            },
          ),
          ListTile(
            leading: Icon(Icons.info_outline, color: Colors.blue[300]),
            title: Text('About Us', style: TextStyle(color: Colors.white)),
            trailing: Icon(Icons.arrow_forward_ios, color: Colors.grey[400], size: 16.0),
            onTap: () {
              // Handle tap
            },
          ),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        backgroundColor: Colors.grey[800],
        selectedItemColor: Colors.blue[300],
        unselectedItemColor: Colors.grey[400],
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.explore),
            label: 'Explore',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.book),
            label: 'Bookings',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.grid_view),
            label: 'Services',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.receipt),
            label: 'Requests',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person),
            label: 'Profile',
          ),
        ],
      ),
    );
  }
}