---
databook:
  created: '2026-04-21'
  hierarchy: 3
  id: Lions-and-Tigers-and-Bears-Oh-My
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:11:04.531130+00:00'
  title: Lions And Tigers And Bears, Oh My!
  type: plain-doc
  version: '0.1'
---

# Lions And Tigers And Bears, Oh My!

[

![](https://substackcdn.com/image/fetch/$s_!9iji!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd44dbbe0-e215-47b1-90a0-776d896c758c_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!9iji!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd44dbbe0-e215-47b1-90a0-776d896c758c_2688x1536.jpeg)

The Shape Constraint Language (SHACL) represents a significant shift in how graphs are specified and modelled. It makes a few very big, fundamental assumptions, not least that classes are no longer primary objects. This can be a real challenge if your first exposure to ontologies came from the use of classes in Protege. This is not to say that you can’t use SHACL in conjunction with OWL or RDFS, only that SHACL does not strictly require either of them.

As described in my previous post,

[https://ontologist.substack.com/p/shacl-node-shapes-and-target-nodes](https://ontologist.substack.com/p/shacl-node-shapes-and-target-nodes)

a Node Shape is simply a pattern in a graph that identifies the nodes to be processed by the SHACL graph. In RDF, we typically use the predicate `rdf:type` to signal that a given node obeys the patterns identified within the RDF _Class_. Because classes play such a big role in both RDFS and OWL, SHACL includes specific properties for identifying them, but it should be noted that you could just as readily use a Node Shape to describe a SKOS concept relationship or could use it to identify an aggregate of several different kinds of classes (or none at all if it came down to it).

The reason is that SHACL is a structural ontology: it makes no implicit assumptions about the availability of a reasoner; it focuses solely on the relationships between graph nodes. This approach is more fundamental and, perforce, means that SHACL tends to be more verbose than OWL or SKOS, but also more precise.

## Inheritance and SHACL

Some areas, such as inheritance, are pretty fundamental to RDFS, but inference chains as rendered with `rdfs:subClassof` and `rdfs:subPropertyOf` can prove to be fairly complex when viewed through the SHACL lens. I’ve talked some about SKOS, but there are properties of SHACL that can address the different components of inheritance.

### Simple Inheritance with `sh:and`

Inheritance is a way of describing a particular design pattern: if a particular class is a subclass of another class, then the subclass inherits the properties of the superclass. The advantage to this approach is that you don’t have to add the same properties from one class to another, but instead can inherit those properties from a more generalised base class.

In SHACL, this is accomplished with the `sh:and` predicate. For instance, consider four shapes that represent animals, mammals, carnivoras, and felinidae (lions, tigers, panthers, leopards, cheetahs, wildcats, and house cats). You can create inheritance by using `sh:and` to identify the super-shape being inherited, binding it with target classes to make things easier to work with

The following illustrates example data that uses this inheritance mechanism:

[

![](https://substackcdn.com/image/fetch/$s_!CPgk!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa9f25e3-a98b-4a43-98c4-58602d9e1c55_8192x7019.png)

](https://substackcdn.com/image/fetch/$s_!CPgk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa9f25e3-a98b-4a43-98c4-58602d9e1c55_8192x7019.png)

This provides validation inheritance, where the properties that are valid are added not only based on what is defined for the shape in question (tied to the associated class), but also on properties of superclasses.

It’s worth noting that `sh:and` always takes a linked list as an object, even if there is only one item in the list - you can’t pass a single IRI here.

[

![](https://substackcdn.com/image/fetch/$s_!3sxV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff89478b7-a4e7-4409-b4e6-b56c6be89d5a_2688x1536.jpeg)

](https://substackcdn.com/image/fetch/$s_!3sxV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff89478b7-a4e7-4409-b4e6-b56c6be89d5a_2688x1536.jpeg)

Why not use `rdfs:subClassOf` directly? In an open world model, especially when dealing with known ontologies, there’s actually no reason why you can’t. It’s only when the model is closed that things get problematic. The biggest use case against it is the situation where you have data in a workflow that may not yet have been assigned a class (which occurs frequently when incoming data hasn’t been categorised yet). In that particular case, the sh:targetClass property would not be specified in the shape:

Here, the node would be tested to see if it had the relevant properties for the shape, and if it passed validation for that node (which still contains the `sh:and` SHACL property), then it would be indicated that the node validated against the Mammal shape as well as any inherited shapes. This means that a dog would be validated as a carnivore, a mammal, and an animal, but wouldn’t necessarily be validated as a cat (cats may (usually do) have retractable claws and hence have that property, while dogs don’t have retractable claws and so don’t have the property).

In general, if you are working with classes, incorporating something like:

does not hurt. Indeed, you can make the associations even stronger (though without any formal SHACL processing) by using a reification on the subclass statement:

I think there is some merit in this design pattern, to be honest. It provides a direct link between inferential subclassing and SHACL structural definitions and validation, as well as descriptive metadata. This means that once you have a subclass relationship, you can get properties and other metadata easily:

This would then produce the following:

[

![](https://substackcdn.com/image/fetch/$s_!ZxoS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F194929c6-093a-4320-91e8-510c9a222c5e_881x391.png)

](https://substackcdn.com/image/fetch/$s_!ZxoS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F194929c6-093a-4320-91e8-510c9a222c5e_881x391.png)

## Summary

There is very seldom an either/or decision to be made with SHACL; you can frequently support common RDFS or OWL inference patterns and class architecture while also incorporating SHACL to better support validation and structure, or when dealing with ingestion-based processing, where you have to infer classes based upon properties and constraints because the classes are unknown.

The `sh:and` SHACL property becomes the workhorse that makes this happen, but it’s only one of several conditional expressions that can be used to create much more robust property shapes and constraints in SHACL. I’ll be covering the rest of these in my next post on SHACL 1.2.

The use of reified annotations dramatically expands what can be done with regard to subclass (and subproperty) relationships, particularly in SHACL. This is another topic for an article which I’ll return to in a future post.

Finally, SHACL changes the way that we think about ontologies in general. Conditional and contextual expressions make models considerably more fluid, and this, in turn, makes the graph more like a state machine than a static graph.

In Media Res,

[

![](https://substackcdn.com/image/fetch/$s_!Zlql!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2abd3153-4086-4b5f-9851-ec62cc2d3acc_2048x2048.jpeg)

](https://substackcdn.com/image/fetch/$s_!Zlql!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2abd3153-4086-4b5f-9851-ec62cc2d3acc_2048x2048.jpeg)

[Kurt Cagle](https://linkedin.com/in/kurtcagle)

[The Ontologist](https://ontologist.substack.com/)

If you like these articles, please consider becoming a paid subscriber. It helps support me so that I can continue writing code, in-depth analyses, educational pieces, and more.

Check out my LinkedIn newsletter, [The Cagle Report](https://www.linkedin.com/newsletters/the-cagle-report-6672594836610252800/).

I am also currently seeking new projects or work opportunities. If anyone is looking for a CTO or Director-level AI/Ontologist, please get in touch with me through my Calendly:

If you want to shoot the breeze or have a cup of virtual coffee, I have a Calendly account at [https://calendly.com/theCagleReport](https://calendly.com/theCagleReport). I am available for consulting and full-time work as an ontologist, AI/Knowledge Graph guru, and coffee maker. Also, for those of you whom I have promised follow-up material, it’s coming; I’ve been dealing with health issues of late.

I’ve created a [Ko-fi account](https://ko-fi.com/E1E117YF5K) for voluntary contributions, either one-time or ongoing, or you can subscribe directly to [The Ontologist](https://ontologist.substack.com/). If you value my articles, technical pieces, or general reflections on work in the 21st century, please consider contributing to support my work and allow me to continue writing.


