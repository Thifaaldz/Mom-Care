import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,

      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        automaticallyImplyLeading: false,
        title: const Text(
          "Kontrol Ibu Hamil",
          style: TextStyle(
            fontWeight: FontWeight.bold,
            color: Colors.black,
            fontSize: 18,
          ),
        ),
        actions: const [
          Icon(Icons.arrow_back_ios, color: Colors.black, size: 20),
          SizedBox(width: 12),
        ],
      ),

      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Profil Ibu
            ListTile(
              leading: const CircleAvatar(
                radius: 26,
                backgroundImage: AssetImage("assets/mom.jpg"), // ganti sesuai asset
              ),
              title: const Text(
                "Ibu Siti",
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
              ),
              subtitle: const Text("Kehamilan Minggu ke-20"),
            ),

            const SizedBox(height: 12),

            // Status Kesehatan
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 16),
              child: Text(
                "Status Kesehatan",
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
              ),
            ),
            const SizedBox(height: 8),
            SizedBox(
              height: 90,
              child: ListView(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 12),
                children: const [
                  _StatusCard("Berat Badan", "65 kg"),
                  _StatusCard("Tekanan Darah", "120/80 mmHg"),
                  _StatusCard("Denyut Jantung", "85 bpm"),
                ],
              ),
            ),

            const SizedBox(height: 16),

            // Monitoring Janin
            Container(
              margin: const EdgeInsets.symmetric(horizontal: 16),
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.teal.shade50,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                children: [
                  const Text("Kemarin, 24 April 2025",
                      style: TextStyle(color: Colors.black54, fontSize: 13)),
                  const SizedBox(height: 8),
                  const Text("Monitoring Kedua Anda",
                      style: TextStyle(fontSize: 15)),
                  const SizedBox(height: 8),
                  const Text(
                    "8 minggu + 2 hari",
                    style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20),
                  ),
                  const SizedBox(height: 12),
                  Image.asset("assets/baby.png", height: 120), // ganti asset
                  const SizedBox(height: 8),
                  const Text("Panjang: 50.6 cm, berat badan: 3,400 g",
                      style: TextStyle(fontSize: 13)),
                ],
              ),
            ),

            const SizedBox(height: 16),

            // Rekomendasi Artikel
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 16),
              child: Text(
                "Rekomendasi Artikel",
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
              ),
            ),
            const SizedBox(height: 8),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: 3,
              itemBuilder: (ctx, i) => Card(
                margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                elevation: 2,
                child: ListTile(
                  leading: const Icon(Icons.article, color: Colors.teal),
                  title: Text("Artikel Kesehatan ${i + 1}"),
                  subtitle: const Text("Deskripsi singkat artikel..."),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () {
                    // navigasi ke detail artikel
                  },
                ),
              ),
            ),
            const SizedBox(height: 80), // biar tidak ketutup nav bar
          ],
        ),
      ),
    );
  }
}

class _StatusCard extends StatelessWidget {
  final String label;
  final String value;

  const _StatusCard(this.label, this.value);

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 150,
      margin: const EdgeInsets.only(right: 12),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.teal,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(label, style: const TextStyle(color: Colors.white)),
          const SizedBox(height: 6),
          Text(
            value,
            style: const TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.bold,
              fontSize: 18,
            ),
          ),
        ],
      ),
    );
  }
}
