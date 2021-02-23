# Example extraction deck

# Initialise boolean package. 
from ui import *
ui = cvar.uiptr
cv = ui.getEditCellView()
geomBegin(cv)
lib = cv.lib()

print "\n# Loading pcells"
ui.loadPCell(lib.libName(), "N_PSM025")
ui.loadPCell(lib.libName(), "P_PSM025")

# ui.loadPCell(lib.libName(), "pres_ex")
# ui.loadPCell(lib.libName(), "moscap_ex")

print "# Get raw layers"
n_well     = geomGetShapes("n_well", "drawing")
active    = geomGetShapes("active", "drawing")
poly      = geomGetShapes("poly", "drawing")
n_plus      = geomGetShapes("n_plus", "drawing")
p_plus      = geomGetShapes("p_plus", "drawing")
contact      = geomGetShapes("contact", "drawing")
metal1    = geomGetShapes("metal1", "drawing")
via     = geomGetShapes("via", "drawing")
metal2    = geomGetShapes("metal2", "drawing")
#rpo       = geomGetShapes("rpo", "drawing")
#cap       = geomGetShapes("cap", "drawing")

print "# Form derived layers"
bkgnd     = geomBkgnd()
psub      = geomAndNot(bkgnd, n_well)
"""
# If there are no poly resistors, don't bother to process them.
if geomNumShapes(rpo) > 0 :
	pres      = geomAnd(poly, rpo)
	poly     = geomAndNot(poly, rpo)
else :
	poly = poly
"""

gate      = geomAnd(poly, active)
diff      = geomAndNot(active, gate)
ndiff     = geomAnd(diff, n_plus)
pdiff     = geomAnd(diff, p_plus)
ntap      = geomAnd(ndiff, n_well)
ptap      = geomAndNot(pdiff, n_well)
ngate     = geomAnd(gate, n_plus)
pgate     = geomAnd(gate, p_plus)

"""
# If there are no mos capacitors, don't bother to process them.
if geomNumShapes(cap) > 0 :
	mosgate   = geomAndNot(gate, cap)
	ngate     = geomAnd(mosgate, n_plus)
	pgate     = geomAnd(mosgate, p_plus)
	mcap      = geomAnd(gate, cap)
else :
	ngate     = geomAnd(gate, n_plus)
	pgate     = geomAnd(gate, p_plus)
"""

print "# Label nactivees"
# This must be done BEFORE geomConnect.
geomLabel(poly, "potxt", "drawing")
geomLabel(metal1, "m1txt", "drawing")
geomLabel(metal2, "m2txt", "drawing")

print "# Form connectivity"
geomConnect( [
              [ptap, pdiff, psub],
              [ntap, ndiff, n_well],
              [contact, ndiff, pdiff, poly, metal1],
              [via, metal1, metal2],
	     ] )

# Save connectivity to extracted view. Saved layers must be
# ones previously connected by geomConnect. Any derived
# layers must be saved to a named layer (e.g. psub below)
print "# Save interconnect"
saveInterconnect([
                [psub, "psub"],
		n_well,
		[ndiff, "active"],
		[pdiff, "active"],
		[poly, "poly"],
		contact,
		metal1,
		via,
		metal2])

# Extract MOS devices. Device terminal layers *must* exist in
# the extracted view as a result of saveInterconnect.
# In this case we are using pcell devices which will be
# created according to the recognition region polyon.

print "# Extract MOS devices"
extractMOS("N_PSM025", ngate, poly, active, psub)
extractMOS("P_PSM025", pgate, poly, active, n_well)


"""
# Extract resistors. Device terminal layers must exist in
# extracted view as a result of saveInterconnect.
if geomNumShapes(rpo) > 0 :
	print "# Extract poly resistors"
	extractRes("pres_ex", pres, poly)

# Extract MOS capacitors. Device terminal layers must exist in
# extracted view as a result of saveInterconnect.
if geomNumShapes(cap) > 0 :
	print "# Extract MOS capacitors"
	extractMosCap("moscap_ex", mcap, poly, active)

# Extract parasitics. 
extractParasitic(metal1, 1.15e-14, 1.50e-14, "VSS")
#extractParasitic2(metal1, metal2, 2.0e-14, 2.0e-14)
"""
# Exit boolean package, freeing memory
print "# Extraction completed."
geomEnd()

# Open the extracted view
ui.openCellView(lib.libName(), cv.cellName(), "extracted")
