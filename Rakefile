
desc "Update the VM"
task :update => [ 'update:bundle', 'update:library', 'update:provision' ]
namespace :update do

    desc "Update Gems via Bundler"
    task :bundle do
        system 'bundle install >/dev/null'
    end

    desc "Run Librarian Puppet for deps"
    task :library do
        system 'bundle exec librarian-puppet install >/dev/null'
    end

    desc "Run Vagrant Provision on the VM"
    task :provision do
        system 'bundle exec vagrant provision'
    end
end

desc "Create Vagrantfile.local"
task :config do
    if !File.exist? 'Vagrantfile.local'
        ip = [ 10, [*1..254].sample, [*1..254].sample, [*2..254].sample ] * '.'
        File.open('Vagrantfile.local', 'w') { |file| file.write("config.vm.network :hostonly, '#{ip}'\n") }
    end
end

desc "Connect to the VM"
task :connect do
    system 'bundle exec vagrant ssh'
end

desc "Create the VM"
task :create do
    system 'bundle exec vagrant up'
end

desc "Destroy the VM"
task :destroy do
    system 'bundle exec vagrant destroy -f'
end

task :default => [ 'update:bundle', 'update:library', :config, :create, :connect ]

