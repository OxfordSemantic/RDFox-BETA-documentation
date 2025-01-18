# Instructions for refreshing explanation-screenshot.passing

As we release new versions of RDFox, with updated visual styles in the console, screenshots embedded within the documentation may start to look out-of-date, giving a bad impression of the documentation. The following instructions should be followed to produce new versions of the file `explanation-screenshot.png` to replace the version checked into this repository.

1. Clone project https://github.com/OxfordSemTech/CompatibilityDemo and check out tag console-screenshot.
1. Start RDFox and open the Console in a Chrome window with the same proportions as the existing screenshot: 1777 x 875.
1. From Chrome, create data store `default` and import the following files from the CompatibilityDemo repository cloned in step 1:
   - `data/data01.ttl`
   - `data/decoration.ttl`
   - `rules/rules.dlog`
1. Select the import setting to include prefixes. (If any of the imports produce warning, try again: sometimes the file that provides the prefixes, `rules/rules.dlog`, is loaded last, and the second time the prefix is sure to be available).
1. Explain the fact `:provides[:GRS-SRS-sm34_sc4_ps7_g17, :Rotation]`.
1. Uncheck the root fact and check the following nine facts. NB they are the nine checkboxes immediately under the root fact.
    ```
    :cost[:SRS-sm34_sc4_ps7, 121]
    :id[:SRS-sm34_sc4_ps7, "sm34+sc4+ps7"]
    :providedSpeed[:SRS-sm34_sc4_ps7, 800]
    :providedTorque[:SRS-sm34_sc4_ps7, 700]
    :SimpleRotationSolution[:SRS-sm34_sc4_ps7]
    :cost[:g17, 23]
    :Gear[:g17]
    :id[:g17, "g17"]
    :providedGearing[:g17, 19]
    ```
1. Expand the tree node for `:providedSpeed[:SRS-sm34_sc4_ps7, 800]`.
1. Select the same node.
1. Scroll the details pane so the selected fact is near the top of the pane.
1. Resize the tree pane so the "(BIND(CONCAT…" rule fragment is truncated at "sm…" and the graph pane so that the same number of facts are visible on the details pane as the screenshot.
1. Manually arrange the nodes on the graph pane to match the existing image.
