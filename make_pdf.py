from fpdf import FPDF

class CustomPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, 'MASTER SERVICES AGREEMENT - CONFIDENTIAL', 0, 1, 'R')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_realistic_contract():
    pdf = CustomPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # PAGE 1: TITLE & PREAMBLE
    pdf.add_page()
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 15, "MASTER SERVICES AGREEMENT", 0, 1, 'C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, "Effective Date: June 25, 2026", 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "PREAMBLE & PARTIES", 0, 1, 'L')
    pdf.set_font("Arial", size=10)
    preamble = (
        "This Master Services Agreement (\"Agreement\") is entered into and made effective as of the date first "
        "written above, by and between Nexus Tech Solutions LLC, with its principal place of business at "
        "100 Innovation Way, San Francisco, CA 94107 (\"Service Provider\"), and Apex Enterprise Systems Corp, "
        "located at 500 Commerce Boulevard, New York, NY 10001 (\"Client\")."
    )
    pdf.multi_cell(0, 6, preamble)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "SECTION 1: SCOPE OF SERVICES", 0, 1, 'L')
    pdf.set_font("Arial", size=10)
    sec1 = (
        "Service Provider shall perform the consulting, engineering, and support services described in detail "
        "in Statement of Work #1 annexed hereto. All deliverables shall be completed in accordance with the schedules "
        "and milestones agreed upon in the SOW."
    )
    pdf.multi_cell(0, 6, sec1)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "SECTION 2: FEES, PAYMENT & BILLING TERMS", 0, 1, 'L')
    pdf.set_font("Arial", size=10)
    sec2 = (
        "In consideration of the services rendered, Client shall pay Service Provider on a monthly basis. All invoices "
        "shall be issued on the 1st of each month and are payable Net 30. Payment Terms enforce a late fee of 1.5% "
        "interest per month on any outstanding balance. Total professional service fees under SOW #1 shall not exceed "
        "an initial budget of $120,000 USD."
    )
    pdf.multi_cell(0, 6, sec2)
    
    # PAGE 2: CORE LEGAL CLAUSES
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "SECTION 3: TERM & TERMINATION PROTOCOL", 0, 1, 'L')
    pdf.set_font("Arial", size=10)
    sec3 = (
        "This Agreement shall commence on the Effective Date and remain active until its formal Expiration Date set for "
        "December 31, 2029, unless terminated earlier in accordance with this Section. Either party may terminate "
        "this Agreement for convenience by providing a written notice of at least 45 Notice Days to the other party. "
        "Upon termination, Client shall pay for all services rendered up to the date of termination."
    )
    pdf.multi_cell(0, 6, sec3)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "SECTION 4: GOVERNING LAW & JURISDICTION", 0, 1, 'L')
    pdf.set_font("Arial", size=10)
    sec4 = (
        "This Agreement, and all claims or causes of action arising hereunder, shall be governed by, construed, and "
        "enforced in accordance with the laws of the State of California, without regard to its conflict of laws principles. "
        "Any legal proceedings related to this contract shall be brought exclusively in the state or federal courts "
        "located in San Francisco County, California."
    )
    pdf.multi_cell(0, 6, sec4)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "SECTION 5: LIMITATION OF LIABILITY", 0, 1, 'L')
    pdf.set_font("Arial", size=10)
    sec5 = (
        "EXCEPT FOR CLAIMS ARISING OUT OF INDEMNIFICATION OR GROSS NEGLIGENCE, IN NO EVENT SHALL EITHER PARTY BE "
        "LIABLE TO THE OTHER FOR ANY CONSEQUENTIAL, INDIRECT, SPECIAL, OR PUNITIVE DAMAGES. THE MAXIMUM CUMULATIVE "
        "LIABILITY LIMIT OF SERVICE PROVIDER TO CLIENT FOR ALL CLAIMS OR BREACHES ARISING UNDER THIS AGREEMENT IS STRICTLY "
        "LIMITED TO $500,000 USD."
    )
    pdf.multi_cell(0, 6, sec5)
    
    # PAGE 3: CONFIDENTIALITY & WARRANTIES
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "SECTION 6: CONFIDENTIALITY & NON-DISCLOSURE", 0, 1, 'L')
    pdf.set_font("Arial", size=10)
    sec6 = (
        "Each party agrees to maintain the strict confidentiality of all Proprietary Information received from the other "
        "party. Confidentiality terms are fully included and enforced. Neither party shall disclose, reproduce, or use "
        "the other party's Confidential Information for any purpose outside the scope of this contract without prior "
        "written consent."
    )
    pdf.multi_cell(0, 6, sec6)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "SECTION 7: WARRANTIES & REMEDIES", 0, 1, 'L')
    pdf.set_font("Arial", size=10)
    sec7 = (
        "Service Provider warrants that the services will be performed in a professional, workmanlike manner in "
        "accordance with standard industry practices. The active Warranty Period is set at 12 months from the date "
        "of delivery. In the event of a breach of this warranty, Client's sole remedy shall be re-performance of the "
        "defective services."
    )
    pdf.multi_cell(0, 6, sec7)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "SECTION 8: DISPUTE RESOLUTION & ARBITRATION", 0, 1, 'L')
    pdf.set_font("Arial", size=10)
    sec8 = (
        "Any dispute arising out of or related to this Agreement shall be resolved through binding arbitration administered "
        "by the American Arbitration Association (AAA) in accordance with its Commercial Arbitration Rules. The arbitration "
        "ruling shall be final and binding on both parties."
    )
    pdf.multi_cell(0, 6, sec8)
    pdf.ln(10)

    # Signature Block
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(90, 6, "Nexus Tech Solutions LLC (Service Provider)", 0, 0, 'L')
    pdf.cell(90, 6, "Apex Enterprise Systems Corp (Client)", 0, 1, 'L')
    pdf.ln(8)
    pdf.cell(90, 6, "Signature: ______________________", 0, 0, 'L')
    pdf.cell(90, 6, "Signature: ______________________", 0, 1, 'L')
    pdf.cell(90, 6, "Name: Jane Doe, CEO", 0, 0, 'L')
    pdf.cell(90, 6, "Name: John Smith, CTO", 0, 1, 'L')
    
    pdf.output("Sample_Contract.pdf")
    print("Realistic multi-page sample contract created successfully!")

if __name__ == "__main__":
    create_realistic_contract()