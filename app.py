<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sahamify Clone - Kalkulator Harga Wajar</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .result-card { display: none; }
    </style>
</head>
<body class="bg-gray-50 font-sans">

    <nav class="bg-blue-600 p-4 text-white shadow-lg">
        <div class="container mx-auto font-bold text-xl">Sahamify <span class="font-light text-blue-200 text-sm italic">Clone</span></div>
    </nav>

    <div class="container mx-auto px-4 py-10 max-w-2xl">
        <div class="bg-white rounded-xl shadow-md p-8">
            <h1 class="text-2xl font-bold text-gray-800 mb-2 text-center">Kalkulator Harga Wajar</h1>
            <p class="text-gray-500 text-center mb-8 italic">Metode Benjamin Graham Revised</p>

            <div class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700">EPS (Laba Per Saham)</label>
                    <input type="number" id="eps" placeholder="Contoh: 150" class="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Estimasi Pertumbuhan Laba (g) %</label>
                    <input type="number" id="growth" placeholder="Contoh: 10" class="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Harga Pasar Saat Ini (Rp)</label>
                    <input type="number" id="currentPrice" placeholder="Contoh: 2500" class="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500">
                </div>
                <button onclick="calculate()" class="w-full bg-blue-600 text-white font-bold py-3 rounded-md hover:bg-blue-700 transition">Hitung Nilai Intrinsik</button>
            </div>

            <div id="resultCard" class="result-card mt-8 border-t pt-6">
                <div class="text-center">
                    <p class="text-gray-600 uppercase text-xs tracking-widest font-semibold">Harga Wajar Saham:</p>
                    <h2 id="fairValueDisplay" class="text-4xl font-extrabold text-blue-600 mt-2">Rp 0</h2>
                    
                    <div id="badge" class="mt-4 inline-block px-4 py-1 rounded-full text-white font-bold text-sm">
                        Status Saham
                    </div>

                    <p id="description" class="mt-4 text-sm text-gray-600 px-4"></p>
                </div>
            </div>
        </div>
    </div>

    <script>
        function calculate() {
            // Ambil Input
            const eps = parseFloat(document.getElementById('eps').value);
            const growth = parseFloat(document.getElementById('growth').value);
            const currentPrice = parseFloat(document.getElementById('currentPrice').value);
            const yieldRate = 4.4; // SBN/Bond Yield rata-rata standar

            if (isNaN(eps) || isNaN(growth) || isNaN(currentPrice)) {
                alert("Mohon isi semua data dengan angka.");
                return;
            }

            // Rumus Graham: V = EPS * (8.5 + 2g) * 4.4 / Yield
            // Karena Yield saat ini bervariasi, kita asumsikan 6.5 (rata-rata bunga deposito/obligasi)
            const currentYield = 6.5; 
            const fairValue = (eps * (8.5 + 2 * growth) * yieldRate) / currentYield;

            // Tampilkan Hasil
            const resultCard = document.getElementById('resultCard');
            const fairValueDisplay = document.getElementById('fairValueDisplay');
            const badge = document.getElementById('badge');
            const description = document.getElementById('description');

            resultCard.style.display = 'block';
            fairValueDisplay.innerText = "Rp " + Math.round(fairValue).toLocaleString('id-ID');

            // Logika Status
            const marginOfSafety = ((fairValue - currentPrice) / fairValue) * 100;

            if (currentPrice < fairValue) {
                badge.innerText = "UNDERVALUED (MURAH)";
                badge.className = "mt-4 inline-block px-4 py-1 rounded-full text-white font-bold text-sm bg-green-500";
                description.innerText = `Harga saat ini lebih murah dari harga wajarnya. Ada potensi Margin of Safety sebesar ${Math.round(marginOfSafety)}%.`;
            } else {
                badge.innerText = "OVERVALUED (MAHAL)";
                badge.className = "mt-4 inline-block px-4 py-1 rounded-full text-white font-bold text-sm bg-red-500";
                description.innerText = "Harga saat ini sudah melampaui harga wajar. Berhati-hatilah untuk melakukan pembelian.";
            }
        </div>
    </script>
</body>
</html>
