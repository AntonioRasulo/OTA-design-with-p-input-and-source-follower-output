# 0.13um example DRC deck

def printErrors(msg) :
	n = geomGetCount()
	if n > 0 :
		print n, msg

# Initialise DRC package. 
from ui import *
cv = ui().getEditCellView()
geomBegin(cv)

# Get raw layers
n_well     = geomGetShapes("n_well", "drawing")
active    = geomGetShapes("active", "drawing")
poly      = geomGetShapes("poly", "drawing")
n_plus      = geomGetShapes("n_plus", "drawing")
p_plus      = geomGetShapes("p_plus", "drawing")
# rpo       = geomGetShapes("rpo", "drawing")
contact      = geomGetShapes("contact", "drawing")
metal1    = geomGetShapes("metal1", "drawing")
via     = geomGetShapes("via", "drawing")
metal2    = geomGetShapes("metal2", "drawing")


# Form derived layers
gate      = geomAnd(poly, active)
polycon   = geomAnd(poly, contact)
activecon = geomAnd(active, contact)
allcon    = geomOr(polycon, activecon)
all_dop   = geomOr(n_plus, p_plus)
badcon    = geomAndNot(allcon, metal1)
badact    = geomAndNot(active, all_dop)
diff      = geomAndNot(active, gate)
ndiff     = geomAnd(diff, n_plus)
pdiff     = geomAnd(diff, p_plus)
nd_s      = geomAndNot(ndiff, n_well) # NMOS Drain Source diffusions
pd_s      = geomAnd(pdiff, n_well) # PMOS Drain Source diffusions
ntap      = geomAnd(ndiff, n_well)
ptap      = geomAndNot(pdiff, n_well)


ptap_con  = geomAnd(ptap, contact)
ntap_con  = geomAnd(ntap, contact)
ptap_rng  = geomSize(ptap_con, 25)
ntap_rng  = geomSize(ntap_con, 25)
n_act_far = geomAndNot(nd_s, ptap_rng)
p_act_far = geomAndNot(pd_s, ntap_rng)


# Form connectivity
geomConnect( [
              [ntap, ndiff, n_well],
              [contact, ndiff, pdiff, poly, metal1],
              [via, metal1, metal2],
	     ] )

print "Check n_well"
geomWidth(n_well, 1.5, "NW width < 1.5")
geomSpace(n_well, 1.0, samenet, "NW space < 1.0")
geomSpace(n_well, 2.2, diffnet, "NW space < 2.2 (different net)")
geomArea(n_well, 1.0, 9e99, "NW area < 1.0")
# geomNotch(n_well, 1.0,  "NW space < 1.0")


print "Check active"
geomWidth(active, 0.5, "active width < 0.5" )
geomSpace(active, 0.5, 0, "active space < 0.5")
# geomNotch(active, 0.5,  "active space < 0.5")
# geomArea(active, 0.122, "active area < 0.122")
geomSpace(n_well, nd_s, 0.8, 0,"NW space to N+ active < 0.8")
geomEnclose(n_well, pd_s, 0.8, "NW enclosure of P+ active < 0.8")
geomSpace(n_well, ptap, 0.5, 0,"NW space to substrate tap < 0.5")
geomEnclose(n_well, ntap, 0.5, "NW enclosure of well-tap < 0.5")


# geomSpace(active, contact, 0.14)

print "Check poly"
geomWidth(poly, 0.25,"poly width < 0.25")
geomSpace(poly, 0.5,0,"poly space < 0.5")
# geomNotch(poly, 0.5,  "poly space < 0.5")
geomExtension(active, gate, 0.5, "active to poly gate extension < 0.5")
geomExtension(poly, active, 0.8, "poly to active extension < 0.8")
geomSpace(poly, active, 0.2, 0,"poly to active space < 0.2")

# geomSpace(poly, contact, 0.11)

print "Check p_plus"
geomWidth(p_plus, 0.3,"p-plus width < 0.3")
geomSpace(p_plus, 0.3,0,"p-plus space < 0.3")
# geomNotch(p_plus, 0.3, "p-plus space < 0.3")
# geomSpace(active, p_plus, 0.03)
geomEnclose(p_plus, active, 0.3, "p_plus - active overlap < 0.3")
# geomEnclose(p_plus, poly, 0.2)
# geomEnclose(p_plus, contact, 0.09)

saveDerived(badact, "Active must be p-plus or n-plus doped")
saveDerived(n_act_far, "Distance between n-active and sub-tap < 25um")
saveDerived(p_act_far, "Distance between p-active and well-tap < 25um")

print "Check n_plus"
geomWidth(n_plus, 0.3,"n-plus width < 0.3")
geomSpace(n_plus, 0.3,0,"n-plus space < 0.3")
#geomNotch(n_plus, 0.3, "n-plus space < 0.3")
geomEnclose(n_plus, active, 0.3, "n_plus - active overlap < 0.3")

"""geomWidth(n_plus, 0.31)
geomSpace(n_plus, 0.31)
geomSpace(active, n_plus, 0.03)
geomOverlap(n_plus, active, 0.18)
geomEnclose(n_plus, poly, 0.2)
geomEnclose(n_plus, contact, 0.09)
geomEnclose(n_well, n_plus, 0.0)
"""
geomSpace(p_plus, n_plus, 0.5,0,"n_plus - p-plus space < 0.5" )

"""
print "Check rpo"
geomWidth(rpo, 0.43)
geomSpace(rpo, 0.43)
geomArea(rpo, 1.0)
geomEnclose(active, rpo, 0.22)
geomEnclose(rpo, active, 0.22)
"""

print "Check contact"
geomWidth(contact, 0.3, "contact width < 0.3")
geomArea(contact, 0.09, 0.09, "Bad contact size")
geomSpace(contact, 0.4,0,"contact space < 0.4")
geomEnclose(active, contact, 0.2, "active enclosure of contact < 0.2")
geomEnclose(poly, contact, 0.2, "poly enclosure of contact < 0.2")

saveDerived(badcon, "bad contactact")




print "Check metal1"
geomWidth(metal1, 0.5,"metal 1 width < 0.5")
geomSpace(metal1, 0.5, 0,"metal 1 space < 0.5")
#geomNotch(metal1, 0.5, "metal 1 space < 0.5")
# geomEnclose(metal1, contact, 0.0)

geomEnclose(metal1, contact, 0.2,"metal 1 enclosure of contact < 0.2" )


# geomArea(metal1, 0.122)

print "Check via"
geomWidth(via, 0.3, "via width < 0.3")
geomArea(via, 0.09, 0.09, "Bad via size")
geomSpace(via, 0.4,0,"via space < 0.4")
geomEnclose(metal1, via, 0.2,"metal 1 enclosure of via < 0.2" )

print "Check metal2"
geomWidth(metal2, 0.5,"metal 2 width < 0.5")
geomSpace(metal2, 0.5,0,"metal 2 space < 0.5")
#geomNotch(metal2, 0.5, "metal 2 space < 0.5")

"""
n_tap_neg=geomNot(ntap_con)
tst=geomInside(n_tap_neg, n_well) 
print "Bad N_well", geomNumShapes(tst)
"""


geomEnclose(metal2, via, 0.2,"metal 2 enclosure of via < 0.2")
# geomArea(metal2, 0.265)
err_cnt=geomGetTotalCount()+geomNumShapes(badact)+geomNumShapes(n_act_far)+geomNumShapes(p_act_far)  

# Exit DRC package, freeing memory
geomEnd()
if err_cnt==0:
        print "No Errors Detected"
else:
        print  err_cnt, " errors detected"


ui().winFit()
