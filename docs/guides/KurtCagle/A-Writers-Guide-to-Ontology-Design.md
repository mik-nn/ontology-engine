---
title: "Lions and Tigers and Bears, Oh My!"
source: "https://ontologist.substack.com/p/lions-and-tigers-and-bears-oh-my?utm_source=profile&utm_medium=reader2"
date: "Feb 26"
tags: [article]
---

[

![](https://substackcdn.com/image/fetch/$s_!xVKl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff3608a78-cdd4-4620-a588-7e4c4b1759f5_2688x1536.png)

](https://substackcdn.com/image/fetch/$s_!xVKl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff3608a78-cdd4-4620-a588-7e4c4b1759f5_2688x1536.png)

An ontology can seem truly daunting, especially with a class-oriented approach. The tendency in designing such systems is to start from the very foundation - Thing - and then build classes with ever-increasing specificity, using inheritance to add to the properties that are exposed. I’ve concluded, however, that this is actually counterproductive.

Instead, think narratively. Let’s go back to that staple of knowledge graphs, the pizza knowledge graph. The first step is to identify who _you_ are. Are you the customer requesting a pizza over the phone? The person who takes the order? The person who makes the pizza? The delivery person? The owner of the store? Each of these has a different story to tell, and it is in those stories that you can build a language of pizza. Each of these _user journeys_ can tell you a great deal about the requirements of such a language.

## The Customer

_Jane has friends over and decides to order a few pizzas from Pete’s Pizza in Pittsburgh through their online portal. After some debate, they decide to get one large Pete’s Supreme with a thick wheat crust, a thin medium Hawaiian with extra mushrooms, and a Veronica’s Veggie with gluten-free, dairy-free cheese and a cauliflower crust, along with breadsticks and marinara sauce, with sides of ranch and sirracca sauce and a couple of 2-litre sodas. She adds each of these to an online shopping cart, pays with her credit card (kept on file), and is notified in the app that her pizzas will be delivered to her address in 30 minutes. She also uses a $5 off coupon from a previous purchase._

There’s a lot of information, and it’s worth breaking this down into several key questions.

1.  Does Jane have a named account to Pete’s Pizza? If so, what are the keys that the account is known by (phone number, email address, name, etc.)?
    
2.  Which store did she order from? Is this store where she always orders from, or does she pull from several?
    
3.  Does Jane have a particular preference for pizza? How many of each pizza does she order? Does she prefer a specific pizza type or a build-your-own pizza?
    
4.  Does Jane have any obvious allergies or dislikes?
    
5.  How often does Jane order pizza?
    
6.  Does Jane regularly use the coupons that she receives?
    
7.  When was the party for which Jane ordered the pizzas?
    
8.  How does Jane pay for her pizza? Is this information on file? Does she have multiple payment methods, possibly from previous moves?
    

These and similar questions help identify kinds of information as well as relationships and properties. Going back to the story, we can rewrite the above in contextual terms:

```
[Customer:Jane]  -- has event --> [Event:Jane’s Party] —- of type —> [EventType:Party] .
[Store:Petes123] -- chain store of --> [Company:PetesPizza] .
[Store:Petes123] -- in city --> [City:Pittsburgh] .
[Customer:Jane] -- orders through --> [PointOfPurchase:WebPortal] .
[Customer:Jane] -- has account --> [Account:1235912].
[Account:1235912] -- has key --> ["jane@example.com"] -- of type --> [KeyType:Email] .
[Customer:Jane] -- places order --> [Order:8151] -- from store [Store:Petes123] .
[Order:8151] -- has key -->  ["8151"] -- of type --> [KeyType:Order] .
[Order:8151] -- has order time --> ["2025-12-16T17:15:25"] .
[Order:8151] -- has projected delivery time --> [”2025-12-16T17:45:25”] .
[Order:8151] -- has actual delivery time --> [”2025-12-16T17:43:19”] .
[Order:8151] -- has item --> [Item:JanesPizza1], [Item:JanesPizza2], 
                             [Item:JanesPizza3], [Item:CheeseBread],
                             [Item:Soda1],[Item:Soda2]
[Order:8151] --uses coupon --> [Coupon:PetesSupreme5-61256] 
```

There’s likely more that you can extract from the story, but this is sufficient to get an idea about the process.

Here’s a diagram showing this particular view.

[

![](https://substackcdn.com/image/fetch/$s_!UFwc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa971b81c-ee52-4d8b-9051-4eb5aa0ab1d2_3108x2470.png)

](https://substackcdn.com/image/fetch/$s_!UFwc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa971b81c-ee52-4d8b-9051-4eb5aa0ab1d2_3108x2470.png)

A few conventions are used here. The top line in each box (in bold) is indicative of some form of datatype or class, while the bottom line (in regular font) is the label for the entry. The arrows indicate properties, and (with a little bit of modification) indicate a verb or preposition of some sort. For instance, you can follow the path from the blue box (Customer) to the red box as:

```
Jane, a Customer, places an order (#8151) from Petes123, a store, in Pittsburgh, a city.
```

The light yellow boxes are literals, meaning that they are strings that can be interpreted in various ways, such as being a key (a form of local identifier), a date-time, or an email address. Both literals and objects (such as Account::Customer) use the same notation for slightly different purposes, with non-object literals indicating some kind of descriptive type (The example provides a customer account. This notation corresponds pretty closely to Neo4J, for instance, but can also be decomposed for RDF. For now, we’ll ignore how this is done and focus on the model itself.

The dark grey rectangle is a linked list of items, with the individual items in light grey. Linked lists retain order, so the list given in the diagram reflects the order in which each item was selected. The dot-leading arrows indicate the sequence of the ordering. Also note that Item is very generic, and there is considerably more detail there that we will need to explore (and we will), but from the perspective of the customer, they are all just items in an order.

Note that this exercise has surfaced a fair amount of useful information. First, by walking through the narrative, you have also identified the kinds of things that are important to the story, to whit:

-   Customers
    
-   Accounts
    
-   Events
    
-   Points of Purchase
    
-   Orders
    
-   Stores
    
-   Companies
    
-   Cities, and
    
-   Lists
    

This is not to say the list is comprehensive (it’s not), but it surfaces, in a meaningful way, the classes of interest _from the customer’s viewpoint._ One clear benefit of starting with users and user journeys is that they provide an example (what I call an **exemplar**) of the model from that user's perspective.

Additionally, this approach also establishes a process. The customer places an order and applies a coupon. The user (an actor) _acts_. This is critical in process modelling because it is frequently the intent of an actor who initiates a particular process.

This is also where you can test assumptions before locking down a model. For instance, notice that neither the event (the party) nor the point of purchase (the web portal) in the above model seem to be connected to anything else beyond the user. However, you can modify the initial user journey as follows:

```
[Store:Petes123] -- chain store of --> [Company:PetesPizza] .
[Store:Petes123] -- in city --> [City:Pittsburgh] .
[Customer:Jane] -- orders through --> [PointOfPurchase:WebPortal] .
[Customer:Jane] -- has account --> [Account:1235912].
[Account:1235912] -- has key --> [”jane@example.com”] -- of type --> [KeyType:Email] .
[Customer:Jane] -- places order --> [Order:8151] -- from store [Store:Petes123] 
[Customer:Jane]  -- places order --> [Order:8151] -- for event --> [Event::Party:Jane’s Party] .
[Customer:Jane]  -- places order --> [Order:8151] -- via point of purchase --> [PointOfPurchase:WebPortal] .
[Order:8151] -- has key -->  [”8151”] -- of type --> [KeyType:Order] .
[Order:8151] -- has order time --> [”2025-12-16T17:15:25”] .
[Order:8151] -- has projected delivery time --> [”2025-12-16T17:45:25”] .
[Order:8151] -- has actual delivery time --> [”2025-12-16T17:43:19”] .
[Order:8151] -- has item --> [Item:JanesPizza1], [Item:JanesPizza2], 
                             [Item:JanesPizza3], [Item:CheeseBread],
                             [Item:Soda1],[Item:Soda2]
```

This changes our visualisation to the following:

[

![](https://substackcdn.com/image/fetch/$s_!AonK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc4be9263-9046-4ea3-8937-8e5031f522eb_2925x2726.png)

](https://substackcdn.com/image/fetch/$s_!AonK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc4be9263-9046-4ea3-8937-8e5031f522eb_2925x2726.png)

This shift is essential because the initial description does not indicate WHEN the party occurred. In the revised model, we don’t care because we now have information that the order was placed at a specific time and was delivered at a particular time. Since the order was _for_ the event, we have also effectively established the party date, at least relative to the data model the pizza company is interested in.

Note that this is another argument for taking a narrative approach to modelling. One of the most significant problems I’ve seen in many years of working as an information architect is that the User Story is next to worthless, because it fails to tie critical information together. An exemplar is a form of user story - it takes a particular scenario as a narrative and from it can be used to shape the data model necessary to “solve” that user story with as little redundant (or unattainable) information as possible. Pete’s Pizza does not need to know the date and time of Jane’s party, but they do need to know when the order was placed and whether it was delivered. By refactoring the user story, we can test different assumptions about our data model that are often not even remotely obvious when you design an ontology as a series of classes.

Now, let’s take a look at the delivery driver's user journey.

## The Delivery Driver

The order has been called in and the chef has made the pizza (we’ll readdress the process of making the pizzas again in a subsequent post, and also see the following post \[Insert Pizza post here\]).

_Jane, our customer, is placing another order for her role as a Girl Scout Leader, as she is reimbursed for her expenses. As part of this, she needs to add a delivery destination for the pizza. She enters the delivery address (which may be her home address, but doesn’t need to be; in this case, she wants it to be the community centre for her troop) and indicates that this should be the default address for this account. Jerry, the delivery driver, then checks his app to see where the order he has is supposed to be delivered, which pulls the customer's default address from their account. He successfully delivers the pizza, and when he does, the system sends an email to Jane asking her to fill out a survey to determine whether there are any problems and whether she liked the service and the pizza's quality._

This surfaces a couple of additional design choices. One of the first is that Jane as a customer is not the same thing as the account that Jane maintains with Pete’s Pizza. Jane may have more than one account - one for her personal use, and perhaps another role as a Girl Scout Leader for her troop, an account for which she gets reimbursed for her expenses.

The order is going to be tied to which account she uses, as will any coupons that she uses. This changes the model subtly:

[

![](https://substackcdn.com/image/fetch/$s_!ckM1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e8b553b-4a82-4684-a4b5-ec3678f9c9c3_3270x3575.png)

](https://substackcdn.com/image/fetch/$s_!ckM1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e8b553b-4a82-4684-a4b5-ec3678f9c9c3_3270x3575.png)

This illustrates one customer (Jane) with two accounts, shows the relationship between an account and orders, adds in the Deliver driver as another actor, and ties the coupon to the issuing company.

Regarding Jerry the Driver: as an employee, there is no doubt additional metadata such as addresses, wage and tax information, medical insurance and so forth, which could be added if this information was likely to be relevant to the knowledge graph, but employee data is second only to customer data in terms of being very highly standardised. As a general rule of thumb, if the purpose of the knowledge graph is to determine external business data, then most of these are not necessarily relevant to the knowledge graph.

## Optimising the Model

The narrative approach has several key benefits that are worth discussing:

-   By working with an actor model (where actors are typically at the top of the tree), you are more likely to determine which actions those actors can take, then dig deeper to assess classifications and literal values. This means that the core of the model involves actors performing actions on objects (most often contractual or event-driven), with those objects, in turn, defining relationships that better specify the characteristics of the subordinate concepts.
    
-   Actors in this approach are consequently more **rootward**, meaning that they tend to have a lot of outbound connections and relatively few inbound connections.
    
-   Actors do not necessarily have to be human, but they must be able to express intent. This provides an agentic framework for a symbolic knowledge graph.
    
-   Actors typically target contracts, roles, and accounts that often have a mix of inbound and outbound edges.
    
-   The further leafward you go, the more you’re likely to deal with material entities and their associated qualifiers, and the more the balance shifts from outbound predominant links to inbound predominant links.
    
-   The primary weakness of inferential models is that they want to turn everything into class inheritance (which is consistent with set theory) rather than the structural building up of composite entities (which is more consistent with graph theory). There are places where class inheritance is valuable. Still, all too often, this manifests as the desire to create upper ontologies that look good in theory but can become unwieldy when you have many composite classes.
    
-   Make your data tell a story. You should be able to start from any actor and construct a narrative simply by following the arrows. If you can’t, it likely means that there is something wrong with your model (to a certain extent, this holds for large language models as well, which have soft classes but consist primarily of overlapping narratives).
    
-   Build as many exemplars following the user journeys of as many actors as possible, and diagram and test these for narrative cohesiveness. If you are doing your job right, exemplars should overlap. You’re not building the knowledge graph this way, but you’re trying to identify the functional pieces (the shapes) of the model that you are creating.
    

## All Relational Models Are Abstract Models

In data modelling theory, you often see the distinction between logical models (where you are working with the abstract relationships) and physical models (where you encode those classes and relationships in languages such as RDF, OWL, SHACL, XSD, JSON-Schema or even DDL.

I’ve never particularly liked that dichotomy, because any abstract model is simply pseudocode for a physical model (which arguably is what any schema language is). I see more of a distinction between structural schemas (such as SHACL) and inferential schemas (such as OWL), but this is mostly a matter of best practices. Any model is abstract; the question is primarily whether it’s parsable or not.

In the above examples, the purpose of building out exemplars is to identify the things and relationships in a particular knowledge graph domain. Going from the above to building out OWL or SHACL is a reasonably easy translation, but it’s not worth doing until you have identified the things in the system, the relationships, and the constraints that act on both. Building that database of use cases and user journeys is the hardest part, but also the most essential.

## Beware the Legacy Data Beast

One last point. I have seen more knowledge graph projects die because the idea of building a knowledge graph seems to be to take every database, spreadsheet, and document and pour them all into a single data store, then expecting these to become cohesive and interoperable magically. LLMs took this approach, essentially swallowing the Internet to do so, and what has emerged is a schizophrenic mess where no single data model predominates. Output primarily depends on what was fed into the language model, not on whether it is cohesive.

Now, as it turns out, language by itself does have a certain innate cohesion, but it’s relatively weak; this is one of the reasons that you can apply a data model to an LLM and get something that seems structured (it may be garbage data, but at least it’s in a workable format). However, one key benefit of a knowledge graph is that, if designed well, it can produce a cohesive, structured narrative. A typical knowledge graph is much (several orders of magnitude) smaller than the equivalent LLM, so this obviously has environmental and cost benefits as well.

When you willy-nilly drop in different data sources without attempting to create a canonical model, what you end up with is difficult to query, is subject to other rules and constraints depending upon the data set, and may just be poorly or incorrectly modelled. We are reaching a stage with generative AI where it is possible to create syncretic solutions at relatively minimal token costs, primarily by controlling the transformations of data sources (various heresies) into an established orthodoxy that varies from one organisational entity to the next.

Converting data directly with LLMs doesn’t scale well (it requires a significant portion of the model to be maintained in context). Still, if you have context-aware transformations (such as SPARQL Update) into a knowledge graph that can be developed via an LLM, you can get away with far more cost and energy-efficient solutions. This is why taking the time to build narrative exemplars is so critical; it is a necessary first step toward automatically implementing such solutions.

I have an upcoming post where I’ll discuss this in greater detail. Meanwhile, time for pizza.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!k2mG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2c2a1fb-114e-4f71-8d13-ae28cd99aef7_2688x1536.png)

](https://substackcdn.com/image/fetch/$s_!k2mG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2c2a1fb-114e-4f71-8d13-ae28cd99aef7_2688x1536.png)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please get in touch with me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you find value in my articles, technical pieces, or general thoughts about work in the 21st century, please consider contributing to support my work and allow me to continue writing.