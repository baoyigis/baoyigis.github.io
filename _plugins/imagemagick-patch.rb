# Patch to fix jekyll-imagemagick compatibility with jekyll-polyglot
# When Polyglot builds language-specific sites, it creates subprocesses.
# This patch ensures imagemagick doesn't run in those subprocesses to avoid directory conflicts.

Jekyll::Hooks.register :site, :after_init do |site|
  # Check if we're in a Polyglot subprocess (non-default language)
  if site.config['lang'] && site.config['default_lang']
    current_lang = site.config['lang']
    default_lang = site.config['default_lang']

    # Disable imagemagick for non-default languages
    if current_lang != default_lang
      if site.config['imagemagick']
        site.config['imagemagick']['enabled'] = false
        Jekyll.logger.info "ImageMagick:", "Disabled for '#{current_lang}' language build (only running for '#{default_lang}')"
      end
    end
  end
end
