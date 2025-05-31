def build_story_prompt(title: str, part_number: int, total_parts: int, previous_parts: list[str] = None) -> str:
    context = ""
    if previous_parts and part_number > 1:
        context = "\nRingkasan bagian sebelumnya:\n" + "\n".join(previous_parts)
    
    base_prompt = f"""
    Buatkan bagian {part_number} dari {total_parts} untuk kisah horor Indonesia dengan judul: {title}
    {context}
    
    Ketentuan untuk bagian ini:
    - Cerita harus berdasarkan pengalaman yang terkesan nyata
    - Gunakan sudut pandang orang pertama ("aku" atau "saya")
    - Panduan untuk lokasi dan setting:
      * Sebutkan hanya nama provinsi
      * Hindari menyebut lokasi spesifik
      * Deskripsikan suasana dan karakteristik daerah tersebut secara detail
      * Gunakan landmark atau ciri khas provinsi tanpa menyebut nama spesifiknya
    - Panduan untuk karakter:
      * Gunakan nama-nama modern Indonesia (hindari nama-nama tradisional Jawa)
      * Setiap karakter harus memiliki kepribadian yang jelas
    - Tambahkan detail-detail realistis seperti:
      * Deskripsi lingkungan yang detail
      * Reaksi emosional yang natural
    - Hindari elemen dongeng atau cerita rakyat
    - Fokus pada kejadian supernatural yang bisa terjadi dalam kehidupan sehari-hari
    - Gunakan bahasa Indonesia yang natural seperti bercerita ke teman
    - Panjang minimal 6000 karakter
    - PENTING: Lanjutkan cerita sesuai dengan bagian sebelumnya pada paragraf terakhir, pastikan alur dan karakter konsisten
    """
    
    if part_number == 1:
        base_prompt += """
        \nIni adalah bagian pembuka cerita:
        - Perkenalkan diri sebagai orang yang mengalami kejadian
        - Jelaskan latar belakang dan situasi awal dengan detail
        - Bangun suasana yang normal sebelum kejadian aneh mulai terjadi"""
    elif part_number == total_parts:
        base_prompt += """
        \nIni adalah bagian klimaks dan penutup:
        - Berikan penyelesaian yang masuk akal namun tetap misterius
        - Sisakan beberapa pertanyaan yang tidak terjawab
        - Tambahkan refleksi pribadi tentang kejadian tersebut"""
    else:
        base_prompt += f"""
        \nIni adalah bagian {part_number}:
        - Kembangkan ketegangan secara bertahap
        - Fokus pada detail-detail mencekam yang subtle
        - Gambarkan reaksi psikologis yang realistis"""
        
    return base_prompt