
<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>
<%@taglib uri="http://jakarta.apache.org/struts/tags-html" prefix="html"%>
<%@taglib uri="http://jakarta.apache.org/struts/tags-bean" prefix="bean"%>
<%@taglib uri="http://jakarta.apache.org/struts/tags-logic" prefix="logic"%>

<%-- DEVELOPMENT NOTE: HOWTO get vaccination update to work. 
    The ClinicalUpdateForm class must have a Vaccination getVaccination(int index)
    for struts to properly update a contained vaccination object.
    " Vaccination[] getVaccination(int index); "  will be usable as a readonly 
    method. So will " List getVaccination(int index); "
--%>
<html>
 
<head><title>JSP Page</title></head>
<body>
<h2> <bean:message key="vacc.entry.heading"/> </h2>

    <logic:present name="vaccines" scope="session">
        <b> Got to here </b>
        
        <html:form action="/SaveClinical"  >    
         <html:text property="test"/> 
        <%-- <html:text property="vaccinations"/> --%>

            <table>
                <tr>
                <bean:message key="vacc.entry.prompt"/>
                </tr>
                
                <logic:iterate id="vaccination" name="clinicalUpdateForm" property="vaccinations" scope="request" >
           
                    <tr>
                    
                    
                    <td>
                        <bean:message key="vacc.date.given"/>
                        <html:text name="vaccination" property="dateGivenString" indexed="true" size="8"/>
                    </td>
                     <td><b><bean:message key="vaccine"/> </b>:</td>
                    <td>
                   
                    <html:select name="vaccination" property="vaccineGiven" indexed="true"  >
                      <html:option key=" " value=" "/>
                      <html:optionsCollection name="vaccines" label="descriptiveName" value="tradeName"   />
                      
                    </html:select>
                    </td>
                    <td>
                        <bean:message key="vacc.batch.no"/>
                        <html:text name="vaccination" property="batchNo" indexed="true" size="6"/>
                    
                        <bean:message key="vacc.site.given"/>
                        <html:text name="vaccination" property="site" indexed="true" size="6"/>
                    </td>
                   
                    </tr>
                </logic:iterate>
            </table>            
<html:submit altKey="change.clinical" ><bean:message key="change.clinical"/></html:submit>
            <html:reset altKey="reset" />
        </html:form>
     
    </logic:present>

</body>



<html:javascript formName="clinicalUpdateForm"
   dynamicJavascript="true" staticJavascript="false"/> 

<script  src="./staticJavascript.jsp"></script>
   
</html>

