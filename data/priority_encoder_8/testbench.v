`timescale 1ns / 1ps

module testbench;
    reg [7:0] in;
    wire [2:0] pos;
    wire valid;
    wire [2:0] expected_pos;
    wire expected_valid;

    top_module dut(.in(in), .pos(pos), .valid(valid));

    // Golden model
    assign expected_valid = |in;
    assign expected_pos = in[7] ? 3'd7 :
                          in[6] ? 3'd6 :
                          in[5] ? 3'd5 :
                          in[4] ? 3'd4 :
                          in[3] ? 3'd3 :
                          in[2] ? 3'd2 :
                          in[1] ? 3'd1 :
                          in[0] ? 3'd0 : 3'd0;

    integer total_samples = 0;
    integer mismatches = 0;

    task check;
        begin
            total_samples = total_samples + 1;
            if (pos !== expected_pos || valid !== expected_valid) begin
                mismatches = mismatches + 1;
                $display("MISMATCH at time %0t: in=%b pos=%0d(exp=%0d) valid=%b(exp=%b)",
                         $time, in, pos, expected_pos, valid, expected_valid);
            end
        end
    endtask

    integer i;
    initial begin
        // Exhaustive test: all 256 input combinations
        for (i = 0; i < 256; i = i + 1) begin
            in = i[7:0]; #10; check;
        end

        $display("Hint: Total mismatched samples is %0d out of %0d samples", mismatches, total_samples);
        if (mismatches == 0) $display("ALL TESTS PASSED");
        else $display("SOME TESTS FAILED");
        $finish;
    end
endmodule
