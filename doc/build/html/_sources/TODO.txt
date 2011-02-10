#######
Roadmap
#######

0.8
===

* add ``utils.py`` and collect some dispersed scripts into this package. **[Done]**
* solve abrveviation problems in the identification of phrases
    ex. "His name is D. Rodrigues and he his a scientist". The dot after D will break a sentence.
    So one needs to be awere of this.
    Another problem is that of the use of hiffens. a "pre-conference" should be treated as 1 word and not as two.
    This things have to be processed at the Document level before breaking the Document into Sentences

0.7.1 **Present Version**
=========================

* corrected :py:meth:`theseus.dtf` method

0.7
===

* add ``fr`` stop words **[Done]**
* add ``es`` stop words **[Done]**
* rename **theseus** module to **processor** and incorporate ``crawler.py`` code into *Theseus* as **crawler** module **[Done]**
* **Documentation** Write what is Thesues section of this documentation. **[Done]**


0.6 
===

* implement :py:meth:`theseus.tfpdf` method **[Done]**
* test :py:meth:`theseus.tfpdf` with text from ECCS'10 Bursaries **[Done]**
* **Documentation** Write the ECCS'10 Bursaries text as an example of usage. **[Done]**

0.5.1
=====
