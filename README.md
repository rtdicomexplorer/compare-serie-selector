# CT Series Selection Pipeline (PACS)

Dieses Projekt zeigt die Pipeline, um die **beste CT-Serie aus PACS** für einen Patienten auszuwählen. 
# CT Series Selection Pipeline (PACS)

Workflow zur Auswahl der besten CT-Serie:

1. **Patient & Diagnose-Datum**  Neme, PIZ, Dates  01-01-2025 (15.02.2025) 30-04-2025  01.05.2025
   ↓
2. **Studien abfragen**
   - CT-Studien
   - Datum: Zeitfenster   or Das richtige DATUM && PIZ
   - Mod-Studies CT
   ↓
3. **Serie-Level filtern**
   - Modality = CT
   - BodyPart passend
   ↓
4. **Image-Level C-FIND**
   - SOPInstanceUIDs abfragen
   - Liste aller Bilder
   ↓
5. **Erstes DICOM holen**
   - Nur erste SOPInstanceUID
   - Minimaler Download
   ↓
6. **Metadaten auslesen**
   - SliceThickness
   - Kernel
   - Orientation
   - KVP
   ↓
7. **Filter & Scoring anwenden**
   - SliceThickness <= 5 mm
   - bevorzugte Phase (venös)
   - andere Kriterien
   ↓
8. **Beste Serie auswählen**
   - Höchster Score
   - Am nächsten vor Therapiebeginn


---

## Hinweise

- **Studienfilter:** CT und Datum → reduziert die Anzahl der möglichen Serien  
- **Serie-Level Filter:** Modality + BodyPart → nur relevante Serien bleiben  
- **Image-Level C-FIND:** Liste aller SOPInstanceUIDs → erste verwenden  
- **Retrieve First Image:** spart Netzwerktraffic und Speicher  
- **Filter & Scoring:** objektive Auswahl der besten Serie  

---
