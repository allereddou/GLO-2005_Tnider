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

doggos = ["http://borkborkiamdoggo.com/wp-content/uploads/2016/12/happy-talk-like-a-pirate-day-1.jpg",
          "https://pics.me.me/pirate-doggo-27554833.png",
          "https://media.wired.com/photos/5a55457ef41e4c2cd9ee6cb5/master/w_2400,c_limit/Doggo-TopArt-104685145.jpg",
          "https://ih0.redbubble.net/image.256560162.4934/flat,800x800,075,f.u8.jpg",
          "https://d3lp4xedbqa8a5.cloudfront.net/s3/digital-cougar-assets/cosmo/2017/03/31/1490937823055_social-doggos.jpg?width=600&height=315&quality=75&mode=crop",
          "https://az616578.vo.msecnd.net/files/2016/11/19/636151440530835523-978948331_doggo.jpg",
          "http://cdn.lifebuzz.com/images/234494/lifebuzz-01b7a47204770ca414d635d4685d84b5-limit_2000.jpg",
          "https://thoughtcatalog.files.wordpress.com/2017/02/dog1.jpg?w=786",
          "https://www.gannett-cdn.com/-mm-/c56eeec9b599ddadbd11e2f604664fcf9ec67bb7/c=12-0-478-350&r=x404&c=534x401/local/-/media/2017/05/17/Louisville/Louisville/636306125477931409-dachsund-in-hood.jpg",
          "https://cdn-images-1.medium.com/max/1600/1*xmJO4mMU2U9iF306EjL22g.jpeg",
          "https://pm1.narvii.com/6273/e2e0709814d60d12d146c8da7b3869ebc202e98f_hq.jpg",
          "http://www.ru-dog.ru/uploads/images/00/00/08/2013/07/30/1bd0e4.jpg",
          "https://pbs.twimg.com/profile_images/778264793031516160/ZB-5sDjq.jpg",
          "https://i.redd.it/4bm184ech64x.jpg",
          "https://i.reddituploads.com/d2c16bb8f6f448bc85619b87cd3d9ceb?fit=max&h=1536&w=1536&s=6f6f30e59a64ec332812499cf3c52c5a",
          "https://images.hellogiggles.com/uploads/2017/12/28015616/merriam-webster-doggo.jpg",
          "http://www.dogbazar.org/wp-content/uploads/2014/09/british-bull-dog-puppies.jpg",
          "https://static.boredpanda.com/blog/wp-content/uploads/2017/09/funny-dog-thoughts-tweets-1.jpg",
          "https://www.cheatsheet.com/wp-content/uploads/2017/05/GettyImages-114304972-640x427.jpg",
          "http://pupjoyblog.com/wp-content/uploads/2017/06/Cute-dog-listening-to-music-1_1.jpg"
          ]

cats = ["https://www.funnypica.com/wp-content/uploads/2015/05/TOP-30-Cute-Cats-Cute-Cat-30.jpg",
        "https://img.diply.com/article-images/a/f4805000-5f86-4594-96ca-c09819be81a7.jpg?impolicy=desktop",
        "http://fenozi.com/wp-content/uploads/2017/04/cute-cats-6.jpg",
        "http://www.smashingphotoz.com/wp-content/uploads/2012/11/11_cat_photos.jpg",
        "http://www.top5ives.com/wp-content/uploads/2012/07/cute-cats-4.jpg",
        "http://i-love-cats.com/images/2015/04/12/cat-wallpaper-24.jpg",
        "http://1.bp.blogspot.com/-l7IXp0s01zQ/UAGDAU6tVcI/AAAAAAAAAVs/h2GZjNgNsno/s1600/kijhi.jpg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRPo32jEVvS_nt44_SJF2Zemfzeawi3aoXd5euN2pvyjt2UG4du",
        "https://cms.hostelbookers.com/hbblog/wp-content/uploads/sites/3/2012/02/search.jpg",
        "https://catzone-tcwebsites.netdna-ssl.com/wp-content/uploads/2014/09/453768-cats-cute.jpg",
        "https://i.pinimg.com/736x/ab/ef/cd/abefcdfd757a47dec9387d0803ab9c2e--friend-photos-cute-cats.jpg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQDQuZP0D_uyoSPP88sdXy9JrJY_ukdb2w3_KIaa94c7e88WBSe",
        "http://darkroom.baltimoresun.com/wp-content/uploads/2013/07/20130709_0103.jpg",
        "http://youne.com/wp-content/uploads/2013/09/grey-kitten.jpg",
        "https://i0.wp.com/lovecuteanimals.com/wp-content/uploads/2017/05/1493782516_254_love-cute-cats.jpg?w=1160&ssl=1",
        "http://babruysk.by/wp-content/uploads/2017/12/%D0%9D%D0%B0%D1%81%D1%82%D1%83%D0%BF%D0%B8%D1%82-%D0%BD%D0%B0%D1%81%D1%82%D0%BE%D1%8F%D1%89%D0%B0%D1%8F-%D0%B7%D0%B8%D0%BC%D0%B0-1.jpg",
        "https://pbs.twimg.com/media/DSAS1uAWkAENbFI.jpg",
        "https://pbs.twimg.com/profile_images/571260078292865024/0EvP5vXn_400x400.jpeg",
        "https://cdn.someecards.com/posts/man-fakes-death-cat-q6U.png",
        "http://media.socastsrm.com/wordpress/wp-content/blogs.dir/886/files/2018/01/PICTURE-OF-CUTE-CAT.jpg",
        "http://www.awwtopia.com/wp-content/uploads/2017/07/Happy-Cat-Month-e1473157690358.jpg",
        "https://www.popsci.com/sites/popsci.com/files/styles/1000_1x_/public/images/2017/08/cat_in_bowl.jpeg?itok=p8hGzKH4&fc=50,50",
        "http://www.top13.net/wp-content/uploads/2016/10/most-beautiful-cats-world-3.jpg"
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
        link = random.choice(doggos)
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
        link = random.choice(cats)
        sql = "INSERT INTO pic(id, caption, link) VALUES ({}, '{}', '{}')"
        cursor.execute(sql.format(results[i]['id'], caption, link))

    sql = "SELECT * FROM pic"
    cursor.execute(sql)
