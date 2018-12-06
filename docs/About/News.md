![tf](../images/tficon-small.png)

# Changes in this major version

???+ hint "Consult the tutorials after changes"
    When we change the API, we make sure that the tutorials shows off
    all possibilities:
    [bhsa]({{etcbcnb}}/bhsa/blob/master/tutorial/start.ipynb)
    [peshitta]({{etcbcnb}}/peshitta/blob/master/tutorial/start.ipynb)
    [syrnt]({{etcbcnb}}/syrnt/blob/master/tutorial/start.ipynb)
    [uruk]({{ninonb}}/uruk/blob/master/tutorial/start.ipynb)

## Queued for next release

??? abstract "TF Browser"
    * The TF kernel/server/website is also fit to be served over the internet
    * There is query result highlighting in passage view (like in SHEBANQ)
    * Various tweaks

??? abstract "TF app API"
    * `prettySetup()` has been replaced with `displaySetup()` and `displayReset()`,
      by which
      you can configure a whole bunch of display parameters selectively.
      **[Display](../Api/App.md#display)**
    * All display functions (`pretty plain prettyTuple plainTuple show table`)
      accept a new optional parameter `withPassage`
      which will add a section label to the display.
      This parameter can be regulated in `displaySetup`. 
      **[Display](../Api/App.md#display)**
    * `A.search()` accepts a new optional parameter: `sort=...`
      by which you can ask for
      canonically sorted results (`True`),
      custom sorted results (pass your onw key function),
      or unsorted results (`False`).
      **[A.search](../Api/App.md#search)**
    * New functions `A.nodeFromSectionStr()` and `A.sectionStrFromNode()`
      which give the passage string of any kind of node, if possible.
      **[Section support for apps](../Api/App.md#sections)**
    * New function `T.sectionTuple(n)` which gives the tuple of section nodes in which `n`
      is embedded
      **[T.sectionTuple](../Api/General.md#sections)**
    * **Modified function `T.sectionFromNode(n, fillup=False)`**
      It used to give a tuple (section1, section2, section3), also for nodes of type
      section1 and section2 (like book and chapter). The new behaviour is the same if
      `fillup=True`. But if `fillup=False` (default), it returns a 1-tuple for
      section1 nodes and a 2-tuple for section2 nodes.
      **[T.sectionFromNode](../Api/General.md#sections)**
    * New API member `sortKeyTuple` to sort tuples of nodes in the
      canonical ordering.
      **[sortKeyTuple](../Api/General.md#navigating-nodes)**
    * The function `T.text()` has a new optional parameter:
      `highlights=set()`.
      Now you can
      highlight parts of plain representations in the same way
      as you can highlight in pretty displays, but still with a few limitations.
      **[T.text](../Api/General.md#text-representation)**
    * The code to detect the file name and path of the script/notebook you are running in,
      is inherently brittle. It is unwise to base decisions on that.
      This code has been removed from TF.
      So TF no longer knows whether you are in a notebook or not.
      And it will no longer produce links to the online
      notebook on GitHub or NBViewer.
    * Various other fixes

??? abstract "Documentation"
    The entry points and paths from superficial to in-depth information have been
    adapted. Writing docs is an uphill battle.

??? abstract "Under the hood"
    As TF keeps growing, the need arises over and over again to reorganize the
    code, weed out duplicate pieces of near identical functionality, and abstract from
    concrete details to generic patterns.
    This release has seen a lot of that.

## 7.1.1

2018-11-21

* Queries in the TF browser are limited to three minutes, after that
  a graceful error message is shown.
* Other small fixes.

## 7.1

2018-11-19

* You can use custom sets in queries in the TF browser
* Reorganized the docs of the individual apps, took the common parts together
* New functions `writeSets` and `readSets` in `tf.lib`

## 7.0.3

2018-11-17

* In the BHSA, feature values on the atom-types and subphrases are now shown too, and that includes extra features
  from foreign data sets
* The feature listing after the incantation in a notebook now lists the loaded modules in a meaningful order.

## 7.0.2

2018-11-16

* Small fixes in `text-fabric-zip`
* Internal reorgnization of the code
* Documentation updates (but internal docs are still lagging behind)

## 7.0.1

2018-11-15

* Fixed messages and logic in finding data and checking for updates (thanks to feedback of Christian Høygaard-Jensen)
* Fixed issue #30
* Improved the doc links under features after the incantation.
* Typos in the documentation

## 7.0.0

2018-11-14

Just before SBL Denver, two years after SBL San Antonio, where I started writing Text-Fabric,
here is major version 7.

Here is what is new:

* you can call in "foreign data": tf feature files made by yourself and other researchers;
* the foreign data shows up in the text-fabric browser;
* all features that are used in a query, show up in the pretty displays in the TF browser,
  also the foreign features;
* there is a command to prepare your own data for distribution via GitHub;
* the incantantion is simpler, but ut has changed in a backwards-incompatible way;
* after the incantation, for each feature it is shown where it comes from.

Under the hood:

* apps (bhsa, peshitta, syrnt, uruk) have been refactored thoroughly;
* a lot of repeated code inside apps has been factored out
* it is easier to turn corpora into new text-fabric apps.

Quick start: the new [share]({{etcbcnb}}/bhsa/blob/master/tutorial/share.ipynb)

See the [v7 guide](../Use/Use7.md) for concrete and detailed hints how to make most of this version.
