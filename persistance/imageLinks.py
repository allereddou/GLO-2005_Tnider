import random


birbs = ["https://i.ytimg.com/vi/R_8bwhiHGHc/hqdefault.jpg", "https://i.ytimg.com/vi/0fLvvYO_C5U/hqdefault.jpg",
         "https://i.ytimg.com/vi/TWw4l347KDI/maxresdefault.jpg", "https://i.ytimg.com/vi/CXROU_gbEMg/maxresdefault.jpg",
         "https://i1.wp.com/www.cutesypooh.com/wp-content/uploads/2017/10/1-NAudFQB-650x650.jpg?resize=600%2C600",
         "https://pics.me.me/thatgirlwiththeguitar-it-me-source-awwww-cute-knit-birb-and-real-birb-28151256.png",
         "https://i0.wp.com/dangriffinyucatan.com/sitenew/wp-content/uploads/2016/06/Amazona_albifrons_-upper_body-8a.jpg?fit=800%2C536",
         "https://vignette.wikia.nocookie.net/animaljam/images/9/9a/Luinifer.jpg/revision/latest?cb=20150920145349",
         "https://assets.change.org/photos/6/dn/fd/NldNfdcEtlICmEs-800x450-noPad.jpg?1478120469",
         "https://pbs.twimg.com/profile_images/927260424050851840/smS_4YO1_400x400.jpg",
         "https://afinde-production.s3.amazonaws.com/uploads/a22e5a8d-9ece-4683-aecf-a9a6c2322270.jpg",
         "https://i.ytimg.com/vi/kCFgrRlAB34/maxresdefault.jpg", "https://i.redd.it/c5rep6h927ny.jpg",
         "https://pics.onsizzle.com/raimbow-birb-25431338.png",
         "https://ih0.redbubble.net/image.226118678.5828/flat,800x800,075,f.u1.jpg",
         "http://www.bharatint.com/img/categories/our-bird-shop-image.png",
         "https://d17fnq9dkz9hgj.cloudfront.net/uploads/2012/11/bird-average-bird-lifespans-thinkstock-155253666.jpg",
         "https://media.nationalgeographic.org/assets/photos/211/752/9f4e06ed-efe2-46ed-b9db-5d54874d3bc8_c5-0-5115-3407_r1032x688.jpg?eaecee55d28eedfaf858fb0ed6ad9a5fe550ea80",
         "https://imgix.ranker.com/user_node_img/50069/1001379050/original/potoo-birds-are-the-subject-of-some-spooky-folklore-photo-u1?w=650&q=50&fm=jpg&fit=crop&crop=faces",
         "http://www.rspcasa.org.au/wp-content/uploads/2015/09/Content_Banner_003_Yellow_bird-600x300-fit-constrain-q70-mobile_banner_image.jpg",
         "https://mymodernmet.com/wp/wp-content/uploads/archive/YI24PaMFeQVPANEjuHIu_1082023271.jpeg"
         ]


def insertBirbPics(cursor):
    sql = "SELECT * FROM bird"
    cursor.execute(sql)

    caption = "This is a test caption"

    results = cursor.fetchall()

    for i in range(len(results)):
        link = random.choice(birbs)
        sql = "INSERT INTO pic(id, caption, link) VALUES ({}, '{}', '{}')"
        cursor.execute(sql.format(results[i]['id'], caption, link))

    sql = "SELECT * FROM pic"
    cursor.execute(sql)

def insertDoggoPics(cursor):
    sql = "SELECT * FROM dog"
    cursor.execute(sql)

    caption = "This is a test caption"

    results = cursor.fetchall()

    for i in range(len(results)):
        link = random.choice(birbs)
        sql = "INSERT INTO pic(id, caption, link) VALUES ({}, '{}', '{}')"
        cursor.execute(sql.format(results[i]['id'], caption, link))

    sql = "SELECT * FROM pic"
    cursor.execute(sql)

def insertKittehPics(cursor):
    sql = "SELECT * FROM cat"
    cursor.execute(sql)

    caption = "This is a test caption"

    results = cursor.fetchall()

    for i in range(len(results)):
        link = random.choice(birbs)
        sql = "INSERT INTO pic(id, caption, link) VALUES ({}, '{}', '{}')"
        cursor.execute(sql.format(results[i]['id'], caption, link))

    sql = "SELECT * FROM pic"
    cursor.execute(sql)


