function lm18_92_PCofSOBS_vs_time_demo()
    format_strings = [
                   "%f" %NUMBER
                   "%f" %DRIVER NUMBER
                   "%f" %LAP NUMBER
                   "%s" %LAP TIME
                   "%f" %IMPROVEMENT
                   "%c" %INLAP
                   "%s" %S1 IMPROVEMENT
                   "%f" %S1
                   "%s" %S2 IMPROVEMENT
                   "%f" %S2
                   "%s" %S3 IMPROVEMENT
                   "%f" %S3
                   "%s" %KPH
                   "%s" %ELAPSED
                   "%s" %HOUR
                   "%s" %S1 LARGE
                   "%s" %S2 LARGE
                   "%s" %S3 LARGE
                   "%s" %TOP SPEED
                   "%s" %DRIVER NAME
                   "%s" %TIME IN PITS
                   "%s" %CLASS
                   "%s" %???GROUP???
                   "%s" %TEAM
                   "%s" %MANUF
                   ];

    DRIVER_NAME_LOCATION = 20;
    LAP_TIME_LOCATION = 4;
    S1_LOCATION = 7;
    S2_LOCATION = 9;
    S3_LOCATION = 11;

    format_string = join(format_strings','');
    result_table = readtable("23_Analysis_Race_Hour 24.csv",'Delimiter','comma','Format',format_string);

    actual_drivers = table2array(result_table(:,DRIVER_NAME_LOCATION));
    driver_names = unique(actual_drivers);
    number_of_drivers = length(driver_names);
    
    subset_92_rows = result_table.NUMBER==92;
    subset_92 = result_table(subset_92_rows,:);
    
    lap_times = table2array(subset_92(:,LAP_TIME_LOCATION));
    actual_laptimes = tableStrCol2MinSecDouble(lap_times);
    
    sector_1 = table2array(subset_92(:,S1_LOCATION));
    actual_sector_1 = tableStrCol2MinSecDouble(sector_1);
    
    sector_2 = table2array(subset_92(:,S2_LOCATION));
    actual_sector_2 = tableStrCol2MinSecDouble(sector_2);
    
    sector_3 = table2array(subset_92(:,S3_LOCATION));
    actual_sector_3 = tableStrCol2MinSecDouble(sector_3);
    
    best_s1 = min(actual_sector_1);
    best_s2 = min(actual_sector_2);
    best_s3 = min(actual_sector_3);
    best_sum_of_sectors = best_s1 + best_s2 + best_s3;
    
    pc_of_potential = actual_laptimes./best_sum_of_sectors;
    
    num_laps = length(actual_laptimes);
    time_elapsed = zeros(num_laps,1);
    
    for inc_laps = 1:num_laps
        time_elapsed = cumsum(actual_laptimes(1:inc_laps));
    end
    
    figure
    plot(time_elapsed./3600,pc_of_potential);
    xlabel("Hour");
    ylabel("% of S.O.B.S");

    function [min_sec_time] = tableStrCol2MinSecDouble(col)
        col_length = length(col);
        min_sec_time = zeros(col_length,1);
        for i = 1:col_length
            if contains(col(i),':')
                [segments,~] = split(col(i),':');
                min_sec_time(i) = str2double(segments(1))*60+str2double(segments(2));
            else
                min_sec_time(i) = str2double(col(i));
            end
        end    
    end

    % function [min_sec_time] = tableStrCol2HourMinSecDouble(col)
    %     [segments,~] = split(col,':');
    %     min_sec_time = str2double(segments(:,1))*60+str2double(segments(:,2));
    % end
end


