# summarize_xml.py

A simple python script that parses an arbitrary XML file and summarizes its schema in a human readable form.

## Summary

It's far from perfect, but it works for me.

I use this when I need to quickly write a parser for an otherwise undocumented XML file.

## Usage

```
$ ./summarize_xml.py <xml file>
```

That's it

## Sample output

### NMAP XML Outout (25Mb source file)

```
nmaprun (startstr, version, xmloutputversion, scanner, start, args)
    debugging (level)
    scaninfo (services, type, numservices, protocol)
    verbose (level)
    taskprogress (etc, task, percent, remaining, time)
    postscript
        script (output, id)
            table (key)
                table (key)
                    elem (key) [has_text]
                elem (key) [has_text]
    host (endtime, starttime)
        status (state, reason, reason_ttl)
        times (to, srtt, rttvar)
        hostnames
            hostname (type, name)
        ports
            extraports (count, state)
                extrareasons (count, reason)
            port (protocol, portid)
                state (state, reason, reason_ttl)
                service (product, version, name, conf, extrainfo, method, ostype, tunnel, devicetype, servicefp, hostname)
                    cpe [has_text]
                script (output, id)
                    table (key)
                        table (key)
                            elem (key) [has_text]
                        elem (key) [has_text]
                    elem (key) [has_text]
        address (addrtype, addr, vendor)
    taskbegin (task, time)
    taskend (task, extrainfo, time)
    runstats
        finished (time, timestr, exit, summary, elapsed)
        hosts (down, total, up)
```

* The tag is always first
* If the tag has attributes, they are included in parenthesis
* If the tag has embeded text it's indicated as has_text in brackets
* If the tag has text tailing its tag, it's indicated as has_tail in brackets

## Embeded Repetition

Since I try to keep the results human readable, it will stop recursing when it detects embeded repeitition.  I don't want to remove all repetition -- some of is useful for understanding the file.  Too much repetition, however, quickly becomes unreadable.

My "final" solution was to not allow "ParentTag+CurrentTag" duplication within a single branch of a tree.  So a tag can be repeated, but only once per parent tag.

### embeded repetition example run across (see Nexpose example, below)

``` 
                ContainerBlockElement [has_text]
                    UnorderedList
                        ListItem [has_text]
                            URLLink (LinkTitle, href, LinkURL) [has_tail, has_text]
                            UnorderedList
                            Paragraph (preformat) [has_text]
                                URLLink (LinkTitle, LinkURL, href) [has_tail, has_text]
                                UnorderedList [has_tail]
                                Paragraph (preformat, preFormat) [has_text]
                                    URLLink (LinkTitle, LinkURL, href) [has_tail, has_text]
                                    UnorderedList [has_tail]
                                    ContainerBlockElement [has_text]
                                        ContainerBlockElement [has_text]
                                            Paragraph (preformat) [has_tail, has_text]
                                                URLLink (LinkTitle, LinkURL, href) [has_tail, has_text]
                                                UnorderedList [has_tail]
                                                OrderedList
                                                    ListItem [has_text]
                                                        OrderedList
```

Using Paragraph and its parents in the above branch as an example:

* ListItem+Paragraph
* Paragraph+Paragraph
* ContainerBlockElement+Paragraph

Those pairings will only show up once and the tree will not descend further, even though the actual data does.  Really beyond this point is no longer useful to me, so drop it.

This is not a perfect solution, but it keeps the output small enough while still being useful.  I originally filtered on a single tag name, as well as depth, but found both solutions limited information.

## More sample output

### Qualys Scanner XML Output (636Mb source file)

```
SCAN (value)
    HEADER
        ASSET_GROUPS
            ASSET_GROUP
                ASSET_GROUP_TITLE [has_text]
        KEY (value) [has_text]
    IP (name, value)
        VULNS
            CAT (protocol, fqdn, value, port)
                VULN (number, severity, cveid)
                    BUGTRAQ_ID_LIST
                        BUGTRAQ_ID
                            URL [has_text]
                            ID [has_text]
                    TITLE [has_text]
                    CVE_ID_LIST
                        CVE_ID
                            URL [has_text]
                            ID [has_text]
                    CVSS_BASE [has_text]
                    SOLUTION [has_text]
                    RESULT [has_text]
                    DIAGNOSIS [has_text]
                    PCI_FLAG [has_text]
        INFOS
            CAT (protocol, fqdn, value, port)
                INFO (number, severity)
                    RESULT [has_text]
                    PCI_FLAG [has_text]
                    TITLE [has_text]
        OS [has_text]
```

Below is an example that includes embeded repetition (removed for readability)

The source file was 253Mb, but the script reduced it to a 200 line schema summary in about 30 seconds.  Editing out the repetition manually took about 30 seconds.

### Rapid7 Nexpose XML v2 output

``` 
NexposeReport (version)
    VulnerabilityDefinitions
        vulnerability (added, cvssScore, severity, title, modified, cvssVector, pciSeverity, published, riskScore, id)
            malware
                name [has_text]
            exploits
                exploit (type, title, link, skillLevel, id)
            description
                [... Manually Truncated -- moved to embeded repetition example ...]
            tags
                tag [has_text]
            solution
                [... Manually Truncated -- moved to embeded repetition example ...]
            references
                reference (source) [has_text]
    nodes
        node (status, address, device-id, site-name, site-importance, risk-score, scan-template, hardware-address)
            endpoints
                endpoint (status, protocol, port)
                    services
                        service (name)
                            tests
                                test (status, vulnerable-since, pci-compliance-status, scan-id, id, key)
                                    [... Manually Truncated -- moved to embeded repetition example ...]
                            fingerprints
                                fingerprint (certainty, version, vendor, product, family)
                            configuration
                                config (name) [has_text]
            tests
                test (status, vulnerable-since, pci-compliance-status, scan-id, id, key)
                    [... Manually Truncated -- moved to embeded repetition example ...]
            fingerprints
                os (device-class, certainty, vendor, product, family, version, arch)
            names
                name [has_text]
            software
                fingerprint (certainty, version, vendor, product, software-class, family)
    scans
        scan (status, endTime, id, startTime, name)
```


