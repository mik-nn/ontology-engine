---
title: "Kurt Cagle"
source: "https://substackcdn.com/image/fetch/$s_!uFS1!,w_1200,h_400,c_pad,f_auto,q_auto:best,fl_progressive:steep,b_auto:border,b_rgb:FFFFFF/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F60c6d44f-8b5b-406a-8818-94d79cd28fc2_1024x1024.png"
date: ""
tags: [article]
---

[

![](https://substackcdn.com/image/fetch/$s_!Bt9g!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99232fb5-356b-4fe8-90f5-46f2bb2badfd_713x447.png)

](https://substackcdn.com/image/fetch/$s_!Bt9g!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99232fb5-356b-4fe8-90f5-46f2bb2badfd_713x447.png)

Recently, the President of the United States, Donald Trump, made a proclamation. Henceforth, the body that was formerly known as the Gulf of Mexico will now be known as the Gulf of America. The previous President, Joe Biden, made a proclamation sometime back that Mt. McKinley in Alaska was to be renamed (or rather reverted to) the name given to it by the Koyukon Athabaskan nations centuries before, Denali. In both cases, there was outrage expressed by groups of people who suddenly found the names of things that they had known inexplicably changed.

## The Changing of Names

Changing names is, of course, not a new phenomenon. Place names, also known as toponyms, change all the time, usually in response to an invading force or distant emperor deciding to put THEIR stamp on the world. The city originally known as Lygos ( c. 800 BC) has since been called Byzantium (657 BC) Augusta Antonina (early 3d Century), Constantinople (330 AD), Stamboul (mid-7th Century), Konstantiniyye and Stamboul with the Ottoman Empire (15th Century), and formally Istanbul in 1930, though the name had been around since the 11th century.

Does a president or prime minister have the authority to change names? This is largely a question of scope. In the United States, a president can issue an executive order directing the changing of a name. In the case of Biden’s move to change the name of the peak known as Demali to Mt. McKinley (named after President McKinley, due to a gold prospector proposing the name change in favor of his favorite candidate at the time), though officially the change didn’t take place until 1910 under William Howard Taft.

Once a president makes this change, it is then sent on to The US Board on Geographic Names (BGN), which controls a registry called the Geographic Names Information System (GNIS). BGN meets, makes the final decision, and incorporates the name into GNIS. This, in turn, is sent to gazeteers and cartographers to make these changes into their existing maps. Such names are considered synonyms - they represent the same core designated entity - though usually the first registered name is accorded reference status. Thus, while Denali is now recognized, internally, the US Government still recognizes this mountain as Mt. McKinley.

There is one major caveat to all of this. These names have to reside within the established boundaries of the United States at the time these names were changed, and if there is a broader authority for geographic naming, then this will retain precedence in all international designations. As it turns out, such a body does exist: the United Nations Group of Experts on Geographical Names (UNGEGN). They serve the same purpose with the UN that BGN does with the United States. This is to prevent a president from naming such things as a major body of water, like the Atlantic Ocean or, gasp, The Gulf of Mexico, to something like the Gulf of Ameria or the Trump Ocean. In that regard, President Trump does not have the authority to change the name of an internationally held body of water (not that this has ever stopped him before).

Ultimately, however, such name changes have more to do with influence than anything. There are around 200,000 Athabaskan speakers in the US and Canada, around which 150,000 are Navajo. Mountain names tend to be notoriously volatile - Mt. Ranier in Washington state was originally known asTa(c)homa by the Salish, before British Explorer George Vancouver (who was responsible for a few place names himself) arrived, in honor of his friend Rear Admiral Peter Ranier. It retains it’s name largely because there is already a city on its northernmost slopes called Tacoma, and as a consequence, there might be (some) confusion, though there’s an active movement in the Puget Sound (named after another of Vancouver’s friends, Lt. Peter Puget) to change the mountain’s name back to Tahoma.

## No Matter Where You Go, There You Are

This is one of the reasons why globally universal semantic identifiers are so important especially when dealing with multiple potential names. For instance, Mount McKinley National Park has a designator gnis:mora

```

@prefix gnis: <https://www.usgs.gov/ngp#>

gnis:1414314 a gnis:Feature ;
    rdfs:label "Mt. Ranier"@en, 
               "Denali"@ath ; # @ath is short for Athabaskan
    .

    
```

where gnis: is the prefix identifying the naming authority for the identifier. As far as I’m aware (and people who know this program PLEASE correct me) that is no formal name for the namespace, so I’m assuming that if it does exist, it will be something similar to the above (ngp is the [National Geospatial Program](https://www.usgs.gov/programs/national-geospatial-program), which is responsible, for, among other things, the [National Map](https://www.usgs.gov/programs/national-geospatial-program/national-map) .

A **naming authority** is simply an organization that maps names to identifiers in an information system. Geonames is a somewhat informal naming authority (it’s largely managed through an ad-hoc group), and both BGB and UNBEGN are naming authorities with scope over the US and global naming conventions for toponyms. This means, in general, that one has to accept a certain degree of **scope** when dealing with naming authorities, specifically which names have precedence under which conditions.

Very recently (within the last decade) the ride-share service Uber spearheaded an initiative to create a universal system for encompassing a region on a globe.

Finding where you are on the planet is complicated. Most people are used to the system that’s evolved over the last couple of centuries specifying a location somewhere on the Earth via latitude/longitude coordinates (sometimes with a height coordinate). This system was initially developed by the Greek scientists Erotosthenes and Hipparchus in the 2nd and 1st centuries BCE, but was considerably refined by Ptolemy in the 2nd century AD. The world knew the Earth was NOT flat long before Columbus, whose biggest mistake (well, one of them) was in believing that the Earth was smaller than it was.

In the 19th century, the British Royal Astronomer, Sir George Airy, established a Prime Meridian (a reference longitudinal position) in Greenwich, England (it was one of many, by the way - many maritime countries in particular created a starting longitude based on their capital). What differentiated Airy’s work was that he also established a working group of many countries that finally agreed (with a lot of argument) to base their origin point on the Greenwich Prime Meridian, and by the 1880s, there was a broad (though not total) consensus on this agreement.

The origin of this particular system (0 degrees latitude, 0 degrees longitude) is off the coast of West Africa in the Gulf of Guinea. This point is designated as Null Island, and is marked by a navigational Buoy as the origin of the Earth’s geospatial system.

![](https://substackcdn.com/image/fetch/$s_!8ScU!,w_720,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F585afa4c-829b-4108-a8de-55607519a33f_1024x967.png)![](https://substackcdn.com/image/fetch/$s_!DVET!,w_720,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7d72a7a3-ca35-43dd-8cd8-c42dad4b97cd_800x948.jpeg)

Null Island

There are three fundamental problems with this system. The first was the fact the flat maps became heavily distorted the closer they were to the poles (something seen in the Mercator Projection of the world, which makes Antarctica and Greenland look far bigger than they were). The second is that the Earth is not a sphere but rather a spheroid. Finally, the Earth is somewhat lumpy, rather than a single gravitational object (in part because it has part of the Mars-sized proto-Moon (Theia) that slammed into the core of Gaia about 4,510 million years ago to form the current Earth, welded to the Earth’s core, in part because of “islands” that are solid chunks within the viscous liquid rock of the Mantle. This makes determining exact positions exciting.

A number of different standards over the years addressed at least some of these issues, resulting in the World Geodetic System being published in 1984 (known by its acronyms WGS-84). WGS-84 became a significant standard for identifying points on the Earth, but it became very awkward to identify regions, as WGS-84 coordinate pairs could get very complicated to render.

## Throwing a Hex Wrench Into The System

In the 2010s, Ride Share service Uber faced a problem - WGS-84 was just not cutting it. Lat-long pairs for describing shapes were computationally very expensive when dealing with whether a given thing was close to (or within) a specific region. It’s possible, using LatLong, to turn the Earth into a grid or tesselation pattern, but defining a grid pattern in that fashion often didn’t mesh well with the ways that cities in particular were laid out (most of whom tend to be roughly circular in nature).

Rectangular grids suffer from distortion in Lat-Long, but they do tile perfectly except around the poles (which was not a use case in their thinking for obvious regions. Other tessellation patterns work better (such as triangular tessellations), but even there, distortion caused issues. Anyone who has ever done tabletop role-playing games has likely encountered hexagonal tiles (tessellations) that are uniform on the plane. Because they are closer to circles than squares, they also fit the need of capturing the typical sprawl of cities, which tend to radiate out from a center.

You cannot completely tile a sphere with any shape, but you can get pretty close with hexagons. At the poles, you have pentagons that form the cap and its surrounding shapes down to a certain longitude (which depends upon the resolution of the tiling). Since the poles tend to be a fairly extreme use case, this makes a tiling system quite useful. Uber proposed the H3 system (H for Hexagons) to do just that.

[

![](https://substackcdn.com/image/fetch/$s_!6Qfh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd606dac-2709-4aea-8d2c-85d91547aa08_1365x598.png)

](https://substackcdn.com/image/fetch/$s_!6Qfh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd606dac-2709-4aea-8d2c-85d91547aa08_1365x598.png)

One other benefit one hexagons is that if you take a hexagon as the boundaries, you can “tile” that with seven more hexagons (a central hexagon and six surrounding hexagons, creating a new finer-grain resolution. From the very largest hexagons, you can go down 15 levels of resolution to the smallest hexagons, which is about 0.6 meters (2 ft) across.

This system, called the H3 system ([https://h3geo.org/](https://h3geo.org/)) then provides a calculatable index from these points, as a 16 byte hexadecimal number. For instance, the peak of Mt. Ranier (aka Mt. Tahoma) is _within_ the hexagon with index “8828d48557fffff”. Notice the distinction here - this does not indicate a _point_ but rather a _region_ on a map. You can then designate an area by identifying all of the relevant tiles that make up a region. At a resolution of 8 this can be rendered as follows (here showing the bulk of the Puget Sound as it crosses between the US and Canada:

[

![](https://substackcdn.com/image/fetch/$s_!cSYU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe19a35e5-d457-4d5c-b51c-7ee4eb2e4f71_438x563.png)

](https://substackcdn.com/image/fetch/$s_!cSYU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe19a35e5-d457-4d5c-b51c-7ee4eb2e4f71_438x563.png)

**The set for this region is then given as:**

```
@prefix gnis: <https://www.usgs.gov/ngp#>

gnis:519201232 a gnis:Feature ;
    rdfs:label "Puget Sound"@en, 
               "Denali"@ath ; # @ath is short for Athabaskan
    gnis:domain "[8428d1dffffffff, 8428d57ffffffff, 8428d0bffffffff, 8428d55ffffffff, 8428d51ffffffff, 8428d5dffffffff, 8428d59ffffffff, 8428d5bffffffff, 8428d19ffffffff, 8428d11ffffffff, 8428d15ffffffff, 8428d17ffffffff, 8428d1bffffffff, 8428c27ffffffff, 8428dc9ffffffff, 8428c25ffffffff, 8428d13ffffffff, 8428de9ffffffff, 8428debffffffff, 8428d8dffffffff, 8428dc7ffffffff, 8428d8bffffffff, 8428d83ffffffff, 8428d81ffffffff, 8428d89ffffffff, 8428dc5ffffffff, 8428dcdffffffff, 8428dc1ffffffff]"^^Unit:H3List ;
   .
```

If two such sets were then compared, it becomes possible to determine whether the regions are distinct, overlapping, or one is completely contained by the other (even if they are at different resolutions). The H3 system includes APIs for mapping any given lat/long point with a spherical boundary to a corresponding H3 index as well as performing the above regional set operations.

Why give this as a list rather than have each hex tile be its own IRI. Part of this is due to the fact that at the deepest resolution, you could be talking about 600 trillion hexagons (about 70% of which are in an ocean). These can theoretically be stored semantically, but they are better off being dereferenced outside of the scope of a graph system.

This diversion is important for a few reasons. First, defining boundaries has always been a very complex problem. By working with an area-centric way of defining a region that can be handled at various levels of revolution, it becomes much easier to indicate what is and is not part of a given jurisdiction. For instance, Italy’s boundaries are fairly well defined, but there is a hole in Rome called Vatican City that is its own country.

Drones and other systems can use such a system to determine where they need to go without the often very complex calculations that are involved with lat-long work (this can especially useful with system telemetry functions that can resolve landmarks into hexes then use that to define “corridors” of access (which is basically how Uber used it).

More to the point here, if you have a way to work with H3 regions, you can use these to bind names to regions so that you can tell whether the names are referring to the same (or mostly the same) features or entities. The defining characteristics shift from naming and linguistic characteristics to regional topologies (especially when regions are in contention). Most deeds and land grants are defined primarily by straight-line surveys, often relying upon historical markers that can change over time (such as rivers, trees, or other buildings). A global, high resolution system such as this makes it easier to establish stable boundaries to arbitrary definitions.

Similarly, such systems can be applied even to virtual worlds, where the authors of those worlds essentially become the naming authority. This will become especially important in shared world environments, where different hosting systems share overlapping world domains. By identifying a set of H3 cells as an IRI, and by acknowledging the naming authority that issues that IRI as being legitimate, you set the stage for land contracts, political agreements, intelligent systems, and other forms of cooperation.

## A Warning on Names

A final thought (and a chilling one). An emperor's goal is acquiring land and, by extension, influence. The act of renaming is a powerful one because it asserts control. During World War II, as the Germans were extending into Western Europe, they frequently renamed French, Flemish, Dutch, and Danish toponyms to German ones, intending to claim territory, and part of the process of indoctrination was to kill or imprison people who refused to recognise those names. Given the authoritarian steps that this administration is taking - exiling people without due process, arresting judges and representatives on Trumped-up charges by unauthorized agents, and so on - it is not at all difficult to assume that the “Gulf of America” is not a lark, but rather a statement of intent to wage war.

It is disappointing that Google, which has perhaps one of the most heavily utilized map systems on the planet, made the change in nomenclature literally days after it was announced. Names also normalise statements, making them appear legitimate, even without consensus. It raises significant questions about the degree to which the company can be considered a legitimate authority.

Civilisation ultimately is built upon establishing checks and balances, and part of that comes down to recognising that others have shared claims on common resources. When countries do not abide by that, they forfeit their protections by being a part of that community, even as controls tighten on people within that pariah state. Names have power. Something to think about.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!bo7w!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff01d5775-b62b-4b7e-bd1d-c96713ca6f08_1456x1456.webp)

](https://substackcdn.com/image/fetch/$s_!bo7w!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff01d5775-b62b-4b7e-bd1d-c96713ca6f08_1456x1456.webp)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker.

I've created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please contribute something to keep me afloat so I can continue writing.