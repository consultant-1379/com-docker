<?xml version="1.0" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output omit-xml-declaration="no" indent="yes"/>
    <xsl:strip-space elements="*"/>

    <xsl:template match="node()|@*">
        <xsl:copy>
            <xsl:apply-templates select="node()|@*"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match='//component'>
        <xsl:for-each select=".">
            <xsl:if test="version/text()">
                <xsl:copy>
                    <xsl:apply-templates/>
                </xsl:copy>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>