def generate_htme_records():
    # Initialize variables
    header_record = ""
    text_records = []
    modification_records = []
    end_record = ""
    current_t_start = None
    current_t_object_code = ""
    current_t_size = 0
    max_t_size = 30  # Max size in bytes
    start_address = None
    lasth=0
    def add_text_record(start, object_code):
        if start is not None and object_code:
            text_records.append(f"T{start:06X}{len(object_code) // 2:02X}{object_code}")

    with open("output_pass2.txt", "r") as file:
        for line in file:
            line = line.strip()

            # Skip empty lines
            if not line:
                # Finish the current T record if any
                add_text_record(current_t_start, current_t_object_code)
                current_t_start = None
                current_t_object_code = ""
                current_t_size = 0
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            if(parts[2]=="END"):
                #print(parts[1])
                u=int(parts[1],16)
                lasth= hex(u)
                continue
            address = int(parts[1], 16)
            object_code = parts[2]
            if start_address is None:
                start_address = address
                program_name = parts[2]

                continue
            last_address = address

            if len(object_code) == 8:  # Format 4 instructions are 4 bytes long
                modification_records.append(f"M{address + 1:06X}05")
            if current_t_start is None:
                current_t_start = address
            if current_t_size + len(object_code) // 2 > max_t_size:
                # Close current T Record
                add_text_record(current_t_start, current_t_object_code)
                # Start a new T Record
                current_t_start = address
                current_t_object_code = object_code
                current_t_size = len(object_code) // 2
            else:
                current_t_object_code += object_code
                current_t_size += len(object_code) // 2
        add_text_record(current_t_start, current_t_object_code)
        program_length = int(lasth,16) - start_address
        u=6-len(program_name)

        while(u!=0):
            program_name+='x'
            u-=1
        # Header Record
        header_record = f"H{program_name:6}{start_address:06X}{program_length:06X}"

        # End Record
        end_record = f"E{start_address:06X}"
        with open("HTME.txt", "w") as output_file:
            output_file.write(header_record + "\n")
            for record in text_records:
                output_file.write(record + "\n")
            for record in modification_records:
                output_file.write(record + "\n")
            output_file.write(end_record + "\n")

generate_htme_records()