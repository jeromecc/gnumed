<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>
<%@taglib uri="http://jakarta.apache.org/struts/tags-html" prefix="html"%>
<%@taglib uri="http://jakarta.apache.org/struts/tags-bean" prefix="bean"%>
<%@taglib uri="http://jakarta.apache.org/struts/tags-logic" prefix="logic"%>
<%@taglib uri="http://jakarta.apache.org/struts/tags-nested" prefix="nested"%>
<%@taglib uri="http://jakarta.apache.org/struts/tags-bean-el" prefix="bean-el"%>

<%@taglib uri="http://jakarta.apache.org/struts/tags-html-el" prefix="html-el"%>
<html>
<head><title>JSP Page</title></head>
<body>


    <h5>Clinical Episode</h5>
  
        <a name="episodeList"/>
  
    <table>
        <logic:iterate   id="episode" 
            name="healthRecord" 
            property="healthSummary.clinEpisodes"
            indexId="index"
            >
            <tr>
            <td>
             
                <bean:write name="episode" property="modified_when" format="dd/MM/yyyy hh:mm" />
            
            </td>
            <td><b>
                <bean:write name="episode" property="description" />
                </b>
                : issue is 
                <bean:write name="episode" property="healthIssue.description"/>
            </td>
            <td>
                <a name='#episodeSummary<%=index%>'/>
                items :
                <nested:iterate id="item" name="episode"
                    property="rootItems"
                        
                    indexId="itemIndex"  >
                        
                    <bean:define    id="itemId"
                    name="item" property="id"/> 
                    <a name="linkItemDetail<%=itemId%>"/>   
 
                    <html-el:link anchor="itemDetail${itemId}"
                        action="ClinicalEdit.do" 
                        paramId="id" 
                        paramName="clinicalUpdateForm" paramProperty="patientId">
                    <%=(itemIndex.intValue() + 1)%>
                    </html-el:link>
             
                </nested:iterate>
            </td>
            </tr>
        </logic:iterate>
    </table>
    <a name="episodeListLast"/>
</body>
</html>
