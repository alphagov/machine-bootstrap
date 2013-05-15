desc "Create Vagrantfile.local"
task :config do
    if !File.exist? 'Vagrantfile.local'
        ip = [ 10, [*1..254].sample, [*1..254].sample, [*2..254].sample ] * '.'
        File.open('Vagrantfile.local', 'w') { |file| file.write("config.vm.network :hostonly, '#{ip}'\n") }
    end
end

task :default => [ :config ]

