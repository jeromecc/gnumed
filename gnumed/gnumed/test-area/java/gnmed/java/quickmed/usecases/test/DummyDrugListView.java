/*
 * DrugListVIew.java
 *
 * Created on 4 August 2003, 02:25
 */

package quickmed.usecases.test;
import java.util.*;
import java.util.logging.*;
import org.drugref.*;
import org.gnumed.gmIdentity.*;
import org.gnumed.gmClinical.*;
/**
 *  This class is the interface between the drug table model and the domain model.
 *  It will create objects and associations for the script problem , as well as providing
 *  the view. ( too many responsibilities ? )
 * @author  sjtan
 *
 */
public class DummyDrugListView implements DrugListView, LimitedViewable, Removable {
    final static String[] VIEWABLE = new String [] { "last","drug","directions", "qty","repeats" };
    private Date last = new Date();
    
    private String directions = "";
    
    private Object drug = "";
    
    private Integer repeats = new Integer(0);
    
    private Integer qty = new Integer(1);
    
    /** Holds value of property identity. */
    private identity identity;
    
    /** Holds value of property identityRef. */
    private Ref identityRef;
    
    /** Holds value of property updating. */
    private boolean updating = true;
    
    private script_drug script_drug;
    
    /** Creates a new instance of DummyDrugListVIew */
    public DummyDrugListView() {
    }
    
    public String getDirections() {
        return directions;
    }
    
    public Object getDrug() {
        return drug;
    }
    
    public Integer getQty() {
        return qty;
    }
    
    public Integer getRepeats() {
        return repeats;
    }
    
    public void setDirections(String directions) {
        Logger.global.info(this + " directions = " + directions);
        this. directions = directions;
        updateIdentity();
    }
    
    public void setDrug(Object drug) {
        Logger.global.info(this + " drug = " + drug.getClass() + ":"+drug);
        this.drug = drug;
        if (drug instanceof package_size) {
            package_size sz = (package_size) drug;
            setQty( new Integer(sz.getSize().intValue()) );
        }
        updateIdentity();
    }
    
    public void setQty(Integer qty) {
        this.qty = qty;
        updateIdentity();
    }
    
    public void setRepeats(Integer repeats) {
        this.repeats = repeats;
    }
    
    public java.util.Date getLast() {
        return last;
    }
    
    public void setLast(java.util.Date last) {
        this.last = last;
    }
    
    /** Getter for property identity.
     * @return Value of property identity.
     *  uses indirection via ref to get the latest set identity.
     */
    public identity getIdentity() {
        if (getIdentityRef() != null) {
            Logger.global.info("USING IDENTITY REF TO RETURN IDENTITY");
            return (identity) getIdentityRef().getRef();
        }
        return this.identity;
    }
    
    /** Setter for property identity.
     * @param identity New value of property identity.
     *
     */
    public void setIdentity(identity identity) {
        this.identity = identity;
    }
    
    public String[] getLimitedView() {
        return VIEWABLE;
    }
    
    /** Getter for property identityRef.
     * @return Value of property identityRef.
     *  this property is used to obtain an identity which is set after the ref is set.
     */
    public Ref getIdentityRef() {
        return this.identityRef;
    }
    
    /** Setter for property identityRef.
     * @param identityRef New value of property identityRef.
     *
     */
    public void setIdentityRef(Ref identityRef) {
        this.identityRef = identityRef;
    }
    
    /**
     * this method looks for the product in the script_drug collection of an identity
     *  and updates a matching script_drug  or creates a new script_drug for the product.
     *  Need to also store the repeats in a link_script_drug sometime soon.
     */
    void updateIdentity() {
        if (getIdentity() == null) {
            Logger.global.severe("IDENTITY IS NULL *********************");
            return;
        }
        
        if (!isUpdating())
            return;
        TestScriptDrugManager manager = TestScriptDrugManager.instance();
        
        /*       ||||||||||||||||||||||||||||||||||
         * replace this with a linked script later.
         */
        script script = new script();
        link_script_drug lsd = new link_script_drug();
        lsd.setRepeats(getRepeats());
        try {
            package_size pz = (package_size) getDrug();
            Double qty = new Double(getQty().doubleValue());
            //try to update.  
            // ************   Meed tp deal with multiple duplicate products as well.
            if (manager.updateIdentityScriptDrugs( getIdentity(), pz.getProduct(), qty,
                                                  getDirections(), getRepeats(), script)
                                                  )
            {
//                showIdentity();
                return;
            }
            
            //else create
            manager.createIdentityScriptDrug( getIdentity(), pz, qty,
                                                                 getDirections(), getRepeats(), script);
            
            showIdentity();
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        
    }
    void showIdentity() {
        
        gnmed.test.DomainPrinter.getInstance().printIdentity(System.out, getIdentity());
    }
    
    public void setScriptDrug(script_drug sd) {
        Logger.global.info("Setting " + this + " with product = " +
            ((generic_drug_name)sd.getPackage_size().getProduct().getDrug_element().getGeneric_name().iterator().next()).getName() +
            "  directions = " + sd.getDirections() );
        
        setDrug(sd.getPackage_size());
        setQty(new Integer(sd.getQty().intValue() ));
        setDirections(sd.getDirections());
        try {if (sd.getLink_script_drugs().iterator().hasNext()) 
            setRepeats(  ( (link_script_drug)sd.getLink_script_drugs().iterator().next()).getRepeats());
        } catch (Exception e) {
            e.printStackTrace();
        }
        this.script_drug = sd;
    }
    
    public script_drug getScriptDrug() {
        return script_drug;
    }
    
    /** Getter for property isUpdating.
     * @return Value of property isUpdating.
     *
     */
    public boolean isUpdating() {
        return this.updating;
    }
    
    /** Setter for property isUpdating.
     * @param isUpdating New value of property isUpdating.
     *
     */
    public void setUpdating(boolean updating) {
        this.updating = updating;
    }
    
    public void remove() {
        TestScriptDrugManager.instance().removeScriptDrug( getIdentity(), getScriptDrug());
    }
    
}
