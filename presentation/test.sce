sampling_rate = 48000;
bits_per_sample = 16;
channels = 2;
write_codes=true;
pulse_width=5;

begin;

sound {
    wavefile {
        filename="440hz.wav";
    };
} snd440;


trial {
    stimulus_event {
		  nothing{};
		  code="";
        port_code=255;
    } test_event;
} main_trial;

trial {
    trial_duration=500;
} isi_trial;

begin_pcl;
output_port OPort = output_port_manager.get_port(1);

loop int i=1 until i>100 begin
    test_event.set_stimulus(snd440);
    main_trial.present();
    isi_trial.present();
	i = i + 1;
end;
